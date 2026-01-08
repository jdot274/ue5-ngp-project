# UE5-NGP Project

## Overview

This repository contains an Unreal Engine 5 project that demonstrates integration with instant-ngp (Instant Neural Graphics Primitives) for creating production-ready applications using NeRF technology for asset generation and real-time rendering.

### Important: NGP's Role in the Pipeline

**instant-ngp is a reconstruction tool, not an asset delivery format.** It processes photogrammetry captures into 3D representations, which are then converted to standard mesh formats (USD/glTF) before being imported into Unreal Engine.

```
[Photogrammetry/Video] → [instant-ngp Processing] → [Mesh Export] → [USD/glTF] → [UE5 Import]
```

**NGP is NOT:**
- A real-time rendering format for UE5
- A replacement for traditional 3D assets
- A general-purpose 3D file format

**NGP IS:**
- An upstream reconstruction tool in your pipeline
- A way to generate high-quality meshes from captures
- Best suited for specific use cases (foliage, rocks, environment details)

## Project Goals

- Build production-ready UE5 applications with photorealistic NeRF-generated assets
- Create a streamlined pipeline from instant-ngp capture/training to UE5 integration
- Develop tooling and plugins to automate asset import and optimization
- Enable workflow for converting neural-rendered scenes into standard 3D formats (USD/glTF)

## Architecture

### Pipeline Overview

The complete workflow positions instant-ngp as an upstream processing tool:

#### 1. Capture Phase
**Tool:** instant-ngp or capture utilities  
**Output:** Raw images, camera poses, point clouds

#### 2. Reconstruction Phase  
**Tool:** instant-ngp training  
**Output:** Neural radiance field representation

#### 3. Export Phase
**Tool:** instant-ngp mesh export or marching cubes  
**Output:** 3D mesh files (OBJ, PLY, etc.)

#### 4. Conversion Phase
**Tool:** USD/glTF conversion tools (Blender, Omniverse, etc.)  
**Output:** USD or glTF files with proper materials and lighting

#### 5. Integration Phase
**Tool:** Unreal Engine 5 USD/glTF importer  
**Output:** Game-ready assets with proper materials and lighting

#### 6. Optimization Phase
**Tool:** UE5 optimization tools (LODs, Nanite, etc.)  
**Output:** Performance-optimized assets for packaging

### When to Use NGP-Generated Assets

**Good Use Cases:**
- Natural foliage and vegetation (trees, bushes, ground cover)
- Rock formations and geological features
- Environmental details and clutter
- Photogrammetry-scanned hero assets
- Scene elements requiring photorealism

**Not Recommended:**
- Characters with animation requirements
- Mechanical/hard-surface objects better suited for CAD
- UI elements or procedurally generated content
- Assets requiring extensive material editing

### Repository Structure

```
ue5-ngp-project/
├── .github/
│   └── workflows/        # CI/CD pipelines
├── Content/
│   ├── Blueprints/       # UE5 Blueprint assets
│   ├── Materials/        # Material definitions
│   ├── Meshes/          # Imported mesh assets
│   ├── NGP/             # NGP-specific configurations
│   └── Maps/            # Level files
├── Plugins/
│   ├── NGPImporter/     # Custom importer plugin
│   └── USDIntegration/  # USD format support
├── Scripts/
│   ├── capture/         # Photogrammetry capture scripts
│   ├── export/          # Mesh export automation
│   ├── convert/         # USD/glTF conversion tools
│   └── batch_import.py  # Batch asset import to UE5
└── Docs/                # Documentation
```

## Prerequisites

- **Unreal Engine 5.1+** (or latest stable)
- **instant-ngp** (installed and configured)
- **Python 3.8+** for automation scripts
- **USD libraries** or **glTF tools** (Blender, USD SDK, etc.)
- **CUDA-capable GPU** (RTX series recommended)
- **Git LFS** for handling large asset files

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/jdot274/ue5-ngp-project.git
cd ue5-ngp-project
```

### 2. Set Up instant-ngp Integration

```bash
# Clone instant-ngp as a submodule or separate repo
git clone https://github.com/NVlabs/instant-ngp.git
cd instant-ngp

# Follow instant-ngp build instructions
cmake . -B build
cmake --build build --config RelWithDebInfo -j
```

### 3. Open UE5 Project

- Open `ue5-ngp-project.uproject` in Unreal Engine 5
- Let the engine compile shaders and assets on first load

## Workflow

### Complete End-to-End Pipeline

#### Step 1: Capture Data

```bash
# Use your camera or phone to capture images
# OR use instant-ngp's video-to-images feature
python scripts/capture/extract_frames.py --input video.mp4 --output captures/
```

#### Step 2: Train with instant-ngp

```bash
# In the instant-ngp directory
./build/testbed --scene ../ue5-ngp-project/captures/

# Train until convergence, then export mesh
# In instant-ngp GUI: Export > Mesh > Save as OBJ/PLY
```

#### Step 3: Convert to USD/glTF

**Option A: Using Blender**
```bash
# Open exported mesh in Blender
# Apply materials, lighting, cleanup
# Export as glTF 2.0 or USD
python scripts/convert/blender_to_gltf.py --input mesh.obj --output asset.gltf
```

**Option B: Using USD Tools**
```bash
# Convert using USD command-line tools
usdcat mesh.obj -o asset.usd
```

#### Step 4: Import to UE5

**Manual Import:**
1. Open UE5 project
2. Content Browser > Import
3. Select USD or glTF file
4. Configure import settings (materials, scale, etc.)
5. Import and place in scene

**Automated Batch Import:**
```bash
# Use provided batch import script
python scripts/batch_import.py --assets ./converted/ --project ./ue5-ngp-project
```

#### Step 5: Optimize in UE5

1. **Enable Nanite** (for supported meshes)
2. **Generate LODs** (for non-Nanite assets)
3. **Optimize materials** (merge textures, reduce draw calls)
4. **Setup lighting** (Lumen or baked lighting)
5. **Test performance** and iterate

### Training with instant-ngp

1. Capture your scene using photos or video
2. Process with instant-ngp:
   ```bash
   ./instant-ngp --scene /path/to/your/images
   ```
3. Train until convergence (typically 30 seconds to 5 minutes)

### Importing to UE5

#### Method A: Direct Mesh Export (Recommended)

1. Export from instant-ngp as mesh (OBJ, PLY, etc.)
2. Convert to USD or glTF using Blender/Omniverse
3. Import into UE5 using native USD/glTF importers

#### Method B: NeRF-to-Mesh Pipeline

1. Export point cloud or volumetric representation
2. Use marching cubes or similar algorithm to generate mesh
3. Optimize and convert to USD/glTF
4. Import optimized mesh into UE5

## Use Cases

### Real-World Applications

This repository demonstrates practical use cases for NGP-generated assets in UE5:

- **Photorealistic Environments:** Generate high-fidelity natural environments from real-world captures
- **Asset Variation:** Create unique variations of foliage, rocks, and clutter
- **Hero Assets:** Produce photogrammetry-quality hero props
- **Rapid Prototyping:** Quickly generate placeholder assets for level design

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Related Projects

- **[instant-ngp](https://github.com/NVlabs/instant-ngp)** - NVIDIA's instant neural graphics primitives
- **[nerfstudio](https://github.com/nerfstudio-project/nerfstudio)** - End-to-end framework for NeRF training and visualization
- **[USD](https://github.com/PixarAnimationStudios/USD)** - Universal Scene Description
- **[glTF](https://www.khronos.org/gltf/)** - GL Transmission Format specification

## Resources

- [Unreal Engine Documentation](https://docs.unrealengine.com/)
- [instant-ngp Paper](https://nvlabs.github.io/instant-ngp/)
- [USD Documentation](https://graphics.pixar.com/usd/docs/index.html)
- [glTF Specification](https://www.khronos.org/registry/glTF/)

## Contact

For questions or collaborations: [@jdot274](https://github.com/jdot274)
