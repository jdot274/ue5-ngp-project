#!/usr/bin/env python3
"""
Batch processing pipeline: NeRF Capture → USD/glTF → UE5

Pipeline stages:
1. NeRF reconstruction (NGP - for complex/organic assets only)
2. Mesh extraction
3. Format conversion (USD + glTF)
4. Ready for UE5 Nanite import
"""

import sys
import subprocess
from pathlib import Path
import argparse


def pipeline_stage(name, cmd, cwd=None):
    """Execute a pipeline stage with error handling"""
    print(f"\n{'='*60}")
    print(f"Stage: {name}")
    print(f"{'='*60}")
    print(f"Command: {' '.join(str(x) for x in cmd)}\n")
    
    result = subprocess.run(cmd, cwd=cwd)
    
    if result.returncode != 0:
        print(f"\n✗ Stage '{name}' failed")
        sys.exit(1)
    
    print(f"\n✓ Stage '{name}' complete")
    return result


def full_pipeline(scene_path, output_name, formats=['usd', 'glb']):
    """
    Complete pipeline from NeRF capture to production assets
    
    Args:
        scene_path: Input NeRF scene data
        output_name: Base name for outputs
        formats: Output formats (usd, glb, or both)
    """
    print("\n" + "#"*60)
    print("# NeRF → USD/glTF → UE5 Production Pipeline")
    print("#"*60)
    print(f"\nInput:  {scene_path}")
    print(f"Output: {output_name}")
    print(f"Formats: {', '.join(formats.upper() for formats in formats)}\n")
    
    # Paths
    raw_dir = Path("Content/NGPAssets/Raw")
    usd_dir = Path("Content/NGPAssets/USD")
    gltf_dir = Path("Content/NGPAssets/glTF")
    
    raw_dir.mkdir(parents=True, exist_ok=True)
    usd_dir.mkdir(parents=True, exist_ok=True)
    gltf_dir.mkdir(parents=True, exist_ok=True)
    
    raw_mesh = raw_dir / f"{output_name}.ply"
    
    # Stage 1: NeRF Reconstruction & Mesh Export
    pipeline_stage(
        "NeRF Training & Mesh Extraction",
        [sys.executable, "export_ngp.py",
         "--scene", scene_path,
         "--output", str(raw_mesh),
         "--train"],
        cwd="Scripts"
    )
    
    # Stage 2: USD Conversion (if requested)
    if 'usd' in formats:
        usd_file = usd_dir / f"{output_name}.usd"
        pipeline_stage(
            "Convert to USD",
            [sys.executable, "convert_to_usd.py",
             str(raw_mesh), str(usd_file)],
            cwd="Scripts"
        )
    
    # Stage 3: glTF Conversion (if requested)
    if 'glb' in formats or 'gltf' in formats:
        gltf_file = gltf_dir / f"{output_name}.glb"
        pipeline_stage(
            "Convert to glTF/GLB",
            [sys.executable, "convert_to_gltf.py",
             str(raw_mesh), str(gltf_file),
             "--format", "glb" if 'glb' in formats else "gltf"],
            cwd="Scripts"
        )
    
    # Summary
    print("\n" + "="*60)
    print("PIPELINE COMPLETE")
    print("="*60)
    print(f"\nAssets ready for UE5 import:")
    if 'usd' in formats:
        print(f"  USD:  {usd_dir / f'{output_name}.usd'}")
    if 'glb' in formats or 'gltf' in formats:
        print(f"  glTF: {gltf_dir / f'{output_name}.glb'}")
    
    print("\nNext Steps:")
    print("  1. Import to UE5 Content Browser")
    print("  2. Enable Nanite (for static meshes)")
    print("  3. Set up materials/lighting")
    print("="*60)


def main():
    parser = argparse.ArgumentParser(
        description='Complete NeRF → USD/glTF → UE5 pipeline'
    )
    parser.add_argument('scene', help='Input NeRF scene path')
    parser.add_argument('--name', required=True, help='Output asset name')
    parser.add_argument(
        '--formats',
        nargs='+',
        choices=['usd', 'glb', 'gltf'],
        default=['usd', 'glb'],
        help='Output formats (default: usd glb)'
    )
    
    args = parser.parse_args()
    full_pipeline(args.scene, args.name, args.formats)


if __name__ == '__main__':
    main()
