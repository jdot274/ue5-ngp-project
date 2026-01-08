#!/usr/bin/env python3
"""
Convert instant-ngp PLY/OBJ exports to USD format for UE5

Usage:
    python convert_to_usd.py input.ply output.usd
    python convert_to_usd.py --batch input_dir/ output_dir/
"""

import os
import sys
import argparse
from pathlib import Path

try:
    import trimesh
    from pxr import Usd, UsdGeom, Sdf, UsdShade
except ImportError as e:
    print(f"Error: Missing required libraries: {e}")
    print("Install with: pip install trimesh usd-core")
    sys.exit(1)


def convert_mesh_to_usd(input_path, output_path, verbose=True):
    """Convert a mesh file (PLY/OBJ) to USD format"""
    if verbose:
        print(f"Loading mesh from {input_path}...")
    
    # Load mesh
    mesh = trimesh.load(input_path)
    
    if verbose:
        print(f"  Vertices: {len(mesh.vertices):,}")
        print(f"  Faces: {len(mesh.faces):,}")
    
    # Create USD stage
    stage = Usd.Stage.CreateNew(str(output_path))
    stage.SetMetadata('upAxis', 'Y')  # UE5 uses Y-up
    stage.SetMetadata('metersPerUnit', 0.01)  # UE5 uses centimeters
    
    # Create mesh
    mesh_name = Path(input_path).stem
    mesh_prim = UsdGeom.Mesh.Define(stage, f'/NGP_Assets/{mesh_name}')
    
    # Set geometry
    mesh_prim.CreatePointsAttr(mesh.vertices.tolist())
    mesh_prim.CreateFaceVertexIndicesAttr(mesh.faces.flatten().tolist())
    mesh_prim.CreateFaceVertexCountsAttr([3] * len(mesh.faces))
    
    # Add normals
    if hasattr(mesh, 'vertex_normals') and mesh.vertex_normals is not None:
        mesh_prim.CreateNormalsAttr(mesh.vertex_normals.tolist())
        mesh_prim.SetNormalsInterpolation('vertex')
    
    # Add UVs if available
    if hasattr(mesh.visual, 'uv') and mesh.visual.uv is not None:
        texCoords = UsdGeom.PrimvarsAPI(mesh_prim).CreatePrimvar(
            'st', Sdf.ValueTypeNames.TexCoord2fArray, UsdGeom.Tokens.faceVarying
        )
        texCoords.Set(mesh.visual.uv.tolist())
    
    # Add vertex colors
    if hasattr(mesh.visual, 'vertex_colors'):
        colors = mesh.visual.vertex_colors[:, :3] / 255.0
        mesh_prim.CreateDisplayColorAttr(colors.tolist())
    
    stage.Save()
    
    if verbose:
        print(f"✓ Exported to {output_path}")


def batch_convert(input_dir, output_dir):
    """Batch convert all PLY/OBJ files"""
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    mesh_files = list(input_dir.glob('*.ply')) + list(input_dir.glob('*.obj'))
    print(f"Found {len(mesh_files)} files to convert\n")
    
    for i, input_path in enumerate(mesh_files, 1):
        print(f"[{i}/{len(mesh_files)}] {input_path.name}")
        output_path = output_dir / f"{input_path.stem}.usd"
        try:
            convert_mesh_to_usd(input_path, output_path, verbose=False)
            print("  ✓ Success\n")
        except Exception as e:
            print(f"  ✗ Error: {e}\n")


def main():
    parser = argparse.ArgumentParser(description='Convert NGP meshes to USD for UE5')
    parser.add_argument('input', help='Input PLY/OBJ file or directory')
    parser.add_argument('output', help='Output USD file or directory')
    parser.add_argument('--batch', action='store_true', help='Batch mode')
    
    args = parser.parse_args()
    
    if args.batch:
        batch_convert(args.input, args.output)
    else:
        convert_mesh_to_usd(args.input, args.output)


if __name__ == '__main__':
    main()
