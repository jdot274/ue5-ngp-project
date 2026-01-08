# UE5-NGP Project

## Overview

This repository contains an Unreal Engine 5 project that integrates with instant-ngp (Instant Neural Graphics Primitives) to create next-generation applications using NeRF technology for asset generation and real-time rendering.

## Project Goals

- Build production-ready UE5 applications with photorealistic NeRF-generated assets
- Create a streamlined pipeline from instant-ngp capture/training to UE5 integration
- Develop tooling and plugins to automate asset import and optimization
- Enable real-time rendering of neural-rendered scenes in Unreal Engine

## Architecture

### Pipeline Overview

1. **Capture Phase**: Use instant-ngp to capture and train NeRF scenes
2. **Export Phase**: Export trained models as meshes, textures, or volumetric data
3. **Import Phase**: Bring assets into UE5 via custom importers or standard formats
4. **Integration Phase**: Integrate into UE5 levels with proper materials and lighting
5. **Optimization Phase**: Optimize for real-time performance and packaging

### Repository Structure

```
ue5-ngp-project/
├── Content/              # UE5 content directory
│   ├── NGPAssets/       # Generated assets from instant-ngp
│   ├── Materials/       # Custom materials for NeRF meshes
│   ├── Blueprints/      # Blueprint logic
│   └── Maps/            # Level maps
├── Plugins/             # Custom UE5 plugins
│   └── NGPImporter/     # Plugin for importing instant-ngp assets
├── Source/              # C++ source code
├── Config/              # Project configuration
├── Scripts/             # Automation scripts
│   ├── export_ngp.py    # Export script for instant-ngp
│   └── batch_import.py  # Batch import to UE5
└── Docs/                # Documentation
```

## Prerequisites

- Unreal Engine 5.3+ (or latest stable)
- instant-ngp installed and configured
- Python 3.8+ for automation scripts
- CUDA-capable GPU (RTX series recommended)
- Git LFS for handling large asset files

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
```

### 3. Open UE5 Project

- Open `ue5-ngp-project.uproject` in Unreal Engine 5
- Let the engine compile shaders and assets on first load

## Workflow

### Training with instant-ngp

1. Capture your scene using photos or video
2. Process with instant-ngp:
   ```bash
   ./instant-ngp data/nerf/your_scene
   ```
3. Train until convergence
4. Export mesh or volumetric representation

### Importing to UE5

1. Export from instant-ngp using provided scripts:
   ```bash
   python Scripts/export_ngp.py --model path/to/model.msgpack --output Content/NGPAssets/
   ```
2. Import into UE5 via Content Browser
3. Apply custom materials optimized for NeRF assets
4. Place in your level

## Development Roadmap

- [ ] Basic UE5 project structure
- [ ] instant-ngp export script
- [ ] Custom UE5 importer plugin
- [ ] Material system for NeRF meshes
- [ ] Example levels and demos
- [ ] Performance optimization tools
- [ ] CI/CD pipeline for automated builds
- [ ] Documentation and tutorials

## CI/CD

### GitHub Actions

This repository uses GitHub Actions for:
- Automated UE5 project builds
- Package creation for Windows/Mac/Linux
- Asset validation
- Plugin compilation

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request with detailed description

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Related Projects

- [instant-ngp](https://github.com/NVlabs/instant-ngp) - NVIDIA's instant neural graphics primitives
- [Unreal Engine](https://www.unrealengine.com/) - Epic Games' game engine

## Resources

- [instant-ngp Documentation](https://github.com/NVlabs/instant-ngp)
- [UE5 Documentation](https://docs.unrealengine.com/5.0/)
- [NeRF Paper](https://www.matthewtancik.com/nerf)

## Contact

For questions or collaboration: [@jdot274](https://github.com/jdot274)
