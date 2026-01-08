#!/usr/bin/env python3
"""
Convert instant-ngp PLY/OBJ exports to glTF format for UE5

Usage:
    python convert_to_gltf.py input.ply output.glb
    python convert_to_gltf.py --batch input_dir/ output_dir/
"""

import os
import sys
import argparse
from pathlib import Path

try:
    import trimesh
except ImportError:
    print("Error: Missing trimesh library")
    print("Install with: pip install trimesh")
    sys.exit(1)


def convert_mesh_to_gltf(input_path, output_path, binary=True, verbose=True):
    """Convert a mesh file (PLY/OBJ) to glTF/GLB format"""
    if verbose:
        print(f"Loading mesh from {input_path}...")
    
    # Load mesh
    mesh = trimesh.load(input_path)
    
    if verbose:
        print(f"  Vertices: {len(mesh.vertices):,}")
        print(f"  Faces: {len(mesh.faces):,}")
    
    # Export to glTF
    file_type = 'glb' if binary else 'gltf'
    
    try:
        mesh.export(
            str(output_path),
            file_type=file_type,
            include_normals=True
        )
    except Exception as e:
        print(f"Error during export: {e}")
        raise
    
    if verbose:
        size_mb = Path(output_path).stat().st_size / 1024 / 1024
        print(f"✓ Exported to {output_path}")
        print(f"  File size: {size_mb:.2f} MB")
        print(f"  Format: {'Binary glTF (GLB)' if binary else 'glTF + textures'}")


def batch_convert(input_dir, output_dir, binary=True):
    """Batch convert all PLY/OBJ files to glTF/GLB"""
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    mesh_files = list(input_dir.glob('*.ply')) + list(input_dir.glob('*.obj'))
    print(f"Found {len(mesh_files)} files to convert\n")
    
    ext = '.glb' if binary else '.gltf'
    
    for i, input_path in enumerate(mesh_files, 1):
        print(f"[{i}/{len(mesh_files)}] {input_path.name}")
        output_path = output_dir / f"{input_path.stem}{ext}"
        
        try:
            convert_mesh_to_gltf(input_path, output_path, binary=binary, verbose=False)
            print("  ✓ Success\n")
        except Exception as e:
            print(f"  ✗ Error: {e}\n")


def main():
    parser = argparse.ArgumentParser(
        description='Convert NGP meshes to glTF/GLB for UE5'
    )
    parser.add_argument('input', help='Input PLY/OBJ file or directory')
    parser.add_argument('output', help='Output glTF/GLB file or directory')
    parser.add_argument('--batch', action='store_true', help='Batch mode')
    parser.add_argument(
        '--format',
        choices=['glb', 'gltf'],
        default='glb',
        help='Output format (default: glb)'
    )
    
    args = parser.parse_args()
    binary = args.format == 'glb'
    
    if args.batch:
        batch_convert(args.input, args.output, binary=binary)
    else:
        convert_mesh_to_gltf(args.input, args.output, binary=binary)


if __name__ == '__main__':
    main()
