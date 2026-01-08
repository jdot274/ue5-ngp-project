#!/usr/bin/env python3
"""
Export meshes from instant-ngp (NeRF/SDF reconstruction tool)

NOTE: instant-ngp is a RECONSTRUCTION ENGINE, not a production asset format.
This script automates the mesh extraction process for downstream USD/UE5 pipelines.

Usage:
    python export_ngp.py --scene data/nerf/my_scene --output exports/my_scene.ply
    python export_ngp.py --train --scene data/nerf/my_scene --iterations 10000
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path


def run_ngp_training(scene_path, output_snapshot, iterations=10000, gui=False):
    """Train a NeRF using instant-ngp"""
    print(f"Training NeRF for {scene_path}...")
    print(f"  Iterations: {iterations}")
    print(f"  Output: {output_snapshot}")
    
    ngp_root = Path("../instant-ngp")  # Adjust to your ngp location
    
    if not ngp_root.exists():
        print(f"Error: instant-ngp not found at {ngp_root}")
        print("Clone it: git clone --recursive https://github.com/nvlabs/instant-ngp")
        sys.exit(1)
    
    cmd = [
        str(ngp_root / "build" / "testbed"),
        "--mode", "nerf",
        "--scene", str(scene_path),
        "--save_snapshot", str(output_snapshot),
        "--n_steps", str(iterations)
    ]
    
    if not gui:
        cmd.append("--no-gui")
    
    print(f"\nRunning: {' '.join(cmd)}\n")
    result = subprocess.run(cmd, cwd=ngp_root)
    
    if result.returncode != 0:
        print(f"Error: Training failed with code {result.returncode}")
        sys.exit(1)
    
    print(f"\n✓ Training complete. Snapshot saved to {output_snapshot}")


def export_mesh_from_ngp(snapshot_path, output_mesh, resolution=512):
    """Extract mesh from trained NeRF using marching cubes"""
    print(f"\nExporting mesh from {snapshot_path}...")
    print(f"  Resolution: {resolution}^3")
    print(f"  Output: {output_mesh}")
    
    ngp_root = Path("../instant-ngp")
    
    # NGP uses Python bindings for mesh export
    script = f"""
import pyngp as ngp

testbed = ngp.Testbed()
testbed.load_snapshot(\"{snapshot_path}\")
testbed.compute_and_save_marching_cubes_mesh(\"{output_mesh}\", resolution={resolution})
print(\"Mesh exported successfully\")
"""
    
    script_path = Path(".ngp_export_temp.py")
    script_path.write_text(script)
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=ngp_root,
            env={**os.environ, "PYTHONPATH": str(ngp_root / "build")}
        )
        
        if result.returncode == 0:
            print(f"\n✓ Mesh exported to {output_mesh}")
            print("\nNext steps:")
            print("  1. Clean mesh in Blender (remesh, decimate)")
            print("  2. Convert to USD: python convert_to_usd.py")
            print("  3. Or convert to glTF: python convert_to_gltf.py")
        else:
            print(f"Error: Mesh export failed")
    finally:
        script_path.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(
        description='Export production meshes from instant-ngp reconstructions'
    )
    parser.add_argument('--scene', required=True, help='Path to NeRF scene data')
    parser.add_argument('--output', help='Output mesh path (PLY format)')
    parser.add_argument('--train', action='store_true', help='Train before export')
    parser.add_argument('--iterations', type=int, default=10000, help='Training iterations')
    parser.add_argument('--resolution', type=int, default=512, help='Mesh resolution')
    parser.add_argument('--gui', action='store_true', help='Show NGP GUI during training')
    
    args = parser.parse_args()
    
    scene_path = Path(args.scene)
    scene_name = scene_path.stem
    
    # Set default output path
    if not args.output:
        args.output = f"Content/NGPAssets/Raw/{scene_name}.ply"
    
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    snapshot_path = output_path.parent / f"{scene_name}.msgpack"
    
    # Training step (if requested)
    if args.train:
        run_ngp_training(
            scene_path,
            snapshot_path,
            iterations=args.iterations,
            gui=args.gui
        )
    elif not snapshot_path.exists():
        print(f"Error: No trained snapshot found at {snapshot_path}")
        print("Run with --train to train first")
        sys.exit(1)
    
    # Mesh extraction
    export_mesh_from_ngp(snapshot_path, output_path, resolution=args.resolution)
    
    print("\n" + "="*60)
    print("NGP RECONSTRUCTION PIPELINE")
    print("="*60)
    print(f"Input:  {scene_path}")
    print(f"Output: {output_path}")
    print("\nNGP Role: Fast NeRF prototyping & mesh extraction")
    print("Next:     Clean mesh → USD/glTF → UE5 Nanite")
    print("="*60)


if __name__ == '__main__':
    main()
