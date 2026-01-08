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


## AI-Assisted Development Features

### Overview

This project includes production-ready AI assistance and remote control capabilities through existing UE5 plugins, enabling external web interfaces and AI-powered development workflows.

### Key Features

#### 1. **UE5 Remote Control Integration**
- **Remote Control API** - Control UE5 properties and functions remotely via REST API
- **Remote Control Web Interface** - Built-in web UI with drag-and-drop interface builder
- **Real-time synchronization** - Multi-client support with live property updates
- **WebSocket events** - Stream real-time engine events to external applications

#### 2. **Pixel Streaming**
- **Viewport streaming** - Stream UE5 viewport over WebRTC to any browser
- **Full input control** - Mouse, keyboard, and touch input from browsers
- **Mobile support** - Works on iOS, Android, and desktop browsers
- **Custom HTML5 UI** - Build custom player interfaces

#### 3. **AI Server**
Production-ready FastAPI server (`AIServer/`) with:
- **Blueprint generation** - AI-powered Blueprint code generation
- **Code assistance** - Generate C++ and Python code for UE5
- **Natural language control** - Control UE5 through conversational AI
- **UE5 Remote Control client** - Complete Python client library for UE5 integration

### Architecture

```
┌─────────────────┐
│  Web Browser    │  ← Pixel Streaming (Live Viewport)
│  (External)     │  ← Remote Control Web UI (Controls)
└────────┬────────┘
         │
         ├─ WebSocket (ws://localhost:80)
         ├─ HTTP REST (http://localhost:7000)
         │
┌────────▼────────┐
│   AI Server     │  ← FastAPI (Port 8000)
│  (Python)       │  ← AI Assistance (Claude/GPT)
└────────┬────────┘
         │
         ├─ Remote Control API
         │
┌────────▼────────┐
│  Unreal Engine  │  ← Remote Control Presets
│     (UE5)       │  ← Pixel Streaming Plugin
│                 │  ← WebUI Widgets
└─────────────────┘
```

### Getting Started with AI Features

#### 1. Enable UE5 Plugins

1. Open your UE5 project
2. Go to **Edit → Plugins**
3. Enable:
   - Remote Control API
   - Remote Control Web Interface  
   - Pixel Streaming
4. Restart Unreal Engine

#### 2. Configure Remote Control

**Project Settings → Plugins → Remote Control:**
```
- Enable Remote Control Web Server: ✓
- Web Server Port: 7000
- Enable Remote Control Web Interface: ✓
```

#### 3. Create Remote Control Presets

1. **Window → Virtual Production → Remote Control**
2. Create a new preset
3. Drag properties/actors you want to control:
   - Camera positions and FOV
   - Light properties (color, intensity)
   - Material parameters
   - Blueprint functions

#### 4. Start the AI Server

```bash
cd AIServer
pip install -r requirements.txt
python server.py
```

The AI server will start on `http://localhost:8000`

#### 5. Access Interfaces

- **Remote Control Web UI**: `http://localhost:7000/remote/control`
- **AI Server API**: `http://localhost:8000/docs`
- **Pixel Streaming**: `http://localhost/` (after starting signaling server)

### Usage Examples

#### Control UE5 from Python

```python
from AIServer.ue5_remote_control import create_client

# Create client
ue5 = create_client(host="localhost", port=7000)

# Check connection
if ue5.health_check():
    print("Connected to UE5!")

# List available presets
presets = ue5.list_presets()
print(f"Available presets: {presets}")

# Set property
ue5.set_property(
    preset_name="MainPreset",
    property_name="CameraActor.FOV",
    value=90
)

# Call Blueprint function
ue5.call_function(
    preset_name="MainPreset",
    function_name="SpawnActor",
    parameters={"ActorClass": "Cube", "Location": {"X": 0, "Y": 0, "Z": 100}}
)

# Batch update properties
ue5.batch_set_properties(
    preset_name="MainPreset",
    properties={
        "Light.Intensity": 5000,
        "Light.Color": {"R": 1.0, "G": 0.8, "B": 0.6},
        "PostProcess.Exposure": 1.2
    }
)
```

#### Stream Real-time Events

```python
import asyncio
from AIServer.ue5_remote_control import stream_ue5_events

async def handle_event(event_data):
    print(f"UE5 Event: {event_data}")
    # Process event, trigger AI response, etc.

# Stream events
await stream_ue5_events(
    host="localhost",
    port=7000,
    event_handler=handle_event
)
```

#### AI-Powered Blueprint Generation

```python
import requests

response = requests.post(
    "http://localhost:8000/api/blueprint/generate",
    json={
        "description": "Create a rotating light that changes color over time",
        "blueprint_type": "Actor",
        "context": {"project": "UE5-NGP"}
    }
)

blueprint = response.json()
print(blueprint["blueprint"])
```

### Production Deployment

#### Remote Control API
- Copy `Engine/Plugins/VirtualProduction/RemoteControlWebInterface/WebApp/` to packaged game
- Configure firewall rules for port 7000
- Enable HTTPS for production

#### Pixel Streaming
- Set up dedicated signaling server
- Configure TURN server for mobile/secure networks
- Use hardware encoding (NVENC/QuickSync)
- Target 30-60 FPS, 1920x1080 resolution

#### AI Server
- Deploy with production ASGI server (Gunicorn + Uvicorn)
- Add authentication and rate limiting
- Use environment variables for API keys
- Set up logging and monitoring

### Documentation

Detailed guides available in `Docs/`:
- **[UE5_PLUGIN_INTEGRATION.md](Docs/UE5_PLUGIN_INTEGRATION.md)** - Comprehensive plugin setup and usage guide
- **[IMPLEMENTATION_PLAN.md](Docs/IMPLEMENTATION_PLAN.md)** - Architecture and implementation details

### API Reference

#### UE5 Remote Control Endpoints

```
GET  /remote/info                 - Server information
GET  /remote/presets               - List all presets
GET  /remote/preset/{name}         - Get preset details
PUT  /remote/object/property       - Set property value
PUT  /remote/object/call           - Call function
GET  /remote/search/assets         - Search for assets
GET  /remote/search/actors         - Search for actors
WS   /remote/events                - WebSocket event stream
```

#### AI Server Endpoints

```
GET  /                             - Server status
POST /api/blueprint/generate       - Generate Blueprint code
POST /api/code/generate            - Generate C++/Python code
POST /api/chat                     - AI chat assistance
WS   /ws                           - WebSocket for real-time communication
```

### Troubleshooting

**Remote Control API not accessible**
- Check Project Settings → Remote Control → Enable Web Server
- Verify port 7000 is not blocked by firewall
- Ensure Remote Control API plugin is enabled

**Pixel Streaming "WebRTC negotiated" but no video**
- Check signaling server is running
- Verify firewall allows WebRTC traffic
- For mobile devices, set up TURN server

**AI Server connection failed**
- Ensure Python dependencies are installed: `pip install -r AIServer/requirements.txt`
- Check AI Server is running on port 8000
- Verify UE5 Remote Control server is accessible

### Resources

- [Remote Control API Documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/remote-control-api-for-unreal-engine)
- [Remote Control Web Interface Guide](https://dev.epicgames.com/documentation/en-us/unreal-engine/remote-control-web-application-for-unreal-engine)
- [Pixel Streaming Documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/pixel-streaming-in-unreal-engine)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
