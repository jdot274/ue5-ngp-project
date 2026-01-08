# UE5 Plugin Integration Guide

This guide explains how to enhance the UE5-NGP project with existing Unreal Engine 5 plugins for remote control, web interfaces, and viewport streaming.

## Overview

Instead of building custom solutions, we leverage Epic's official plugins:
- **Remote Control API** - Expose and control UE5 properties remotely
- **Remote Control Web Interface** - Built-in web UI for controlling UE5
- **Pixel Streaming** - Stream UE5 viewport over WebRTC to browsers
- **WebUI Plugin** (third-party) - HTML/CSS/JS interfaces in UE5

## 1. Remote Control API Setup

### Enable the Plugin

1. Open your UE5 project
2. Go to **Edit → Plugins**
3. Search for "Remote Control"
4. Enable:
   - Remote Control API
   - Remote Control Web Interface
5. Restart Unreal Engine

### Create a Remote Control Preset

1. **Window → Virtual Production → Remote Control**
2. Create a new Remote Control Preset
3. Drag properties/actors you want to control into the preset:
   - Camera positions
   - Light properties
   - Material parameters
   - Blueprint functions

### Configuration

**Project Settings → Plugins → Remote Control:**
```
- Enable Remote Control Web Server: ✓
- Web Server Port: 7000 (default)
- Enable Remote Control Web Interface: ✓
```

### API Endpoints

The Remote Control API exposes RESTful endpoints:

```
GET  http://localhost:7000/remote/info
GET  http://localhost:7000/remote/presets
PUT  http://localhost:7000/remote/object/property
POST http://localhost:7000/remote/object/call
```

### Integration with AIServer

Update `AIServer/server.py` to communicate with UE5 Remote Control:

```python
import requests

UE5_REMOTE_URL = "http://localhost:7000/remote"

async def control_ue5_property(preset_name, property_path, value):
    """Control UE5 property via Remote Control API"""
    response = requests.put(
        f"{UE5_REMOTE_URL}/object/property",
        json={
            "PresetName": preset_name,
            "PropertyName": property_path,
            "PropertyValue": value
        }
    )
    return response.json()

async def call_ue5_function(preset_name, function_name, parameters={}):
    """Call UE5 Blueprint function via Remote Control API"""
    response = requests.post(
        f"{UE5_REMOTE_URL}/object/call",
        json={
            "PresetName": preset_name,
            "FunctionName": function_name,
            "Parameters": parameters
        }
    )
    return response.json()
```

## 2. Remote Control Web Interface

### Access the Built-in Web UI

Once enabled, access at:
```
http://localhost:7000/remote/control
```

### Customize the Web UI

1. The web interface has a built-in UI editor
2. Connect widgets to your Remote Control Preset properties:
   - Sliders for numeric values
   - Color pickers for colors
   - Buttons for functions
   - Text inputs for strings

### Multi-Client Support

The web interface supports multiple simultaneous clients with real-time property sync across all connected users.

### Deployment

For packaged games, copy:
```
Engine/Plugins/VirtualProduction/RemoteControlWebInterface/WebApp/
```
to your packaged game folder under the same path.

## 3. Pixel Streaming Setup

### Enable Pixel Streaming Plugin

1. **Edit → Plugins**
2. Search "Pixel Streaming"
3. Enable **Pixel Streaming** plugin
4. Restart UE5

### Configuration

**Project Settings → Plugins → Pixel Streaming:**
```
- Streamer Port: 8888
- Signaling Server URL: ws://localhost:80
- Enable WebRTC: ✓
```

### Run the Signaling Server

UE5 includes signaling server components:

```bash
cd Engine/Plugins/Media/PixelStreaming/Resources/WebServers/SignallingWebServer
node cirrus.js
```

### Launch with Pixel Streaming

Package or run with:
```
-PixelStreamingURL=ws://127.0.0.1:8888 -RenderOffScreen
```

### Access the Stream

Open browser to:
```
http://localhost/
```

You'll see your UE5 viewport streaming with full input control (mouse, keyboard, touch).

### WebRTC Architecture

```
[UE5 Application] ←→ [Signaling Server] ←→ [Web Browser]
     (WebRTC)              (Port 80)         (HTML5 Player)
```

### Mobile & Network Support

- Works on iOS, Android, desktop browsers
- For secure networks, configure TURN server
- Supports touch input and custom HTML5 UI

## 4. WebUI Plugin (Third-Party)

### Installation

Use Tracer Interactive's WebUI plugin for embedded web interfaces:

1. Download from: https://github.com/tracerinteractive/UnrealWebUI
2. Copy to `Plugins/WebUI/`
3. Rebuild project

### Create Web Interface Widget

1. Create Widget Blueprint
2. Add **Web Interface** component
3. Load URL: `http://localhost:8080` or local HTML file

### Communication Bridge

**JavaScript → UE5:**
```javascript
ue4("functionName", { param1: value1 });
```

**UE5 → JavaScript:**
```cpp
WebInterface->ExecuteJavascript("functionName({data: 'value'})");
```

### Integration with Vue.js/React

See: https://github.com/u4yk/WebUIVue for Vue.js framework integration

## 5. Combined Architecture

### Full System Integration

```
┌─────────────────┐
│  Web Browser    │  ← Pixel Streaming (Viewport)
│  (External)     │  ← Remote Control Web UI (Controls)
└────────┬────────┘
         │
         ├─ WebSocket (ws://localhost:80)
         ├─ HTTP REST (http://localhost:7000)
         │
┌────────▼────────┐
│   AI Server     │  ← FastAPI (Port 8000)
│  (Python)       │  ← AI Assistance
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

### Workflow

1. **User opens web browser**
   - Pixel Streaming tab shows live UE5 viewport
   - Remote Control Web UI tab provides controls

2. **AI Server enhances functionality**
   - Accepts natural language commands
   - Translates to Remote Control API calls
   - Generates Blueprint code
   - Provides intelligent suggestions

3. **UE5 responds in real-time**
   - Properties update instantly
   - All clients see synchronized changes
   - Viewport streams to all connected browsers

## 6. Deployment Checklist

### Development
- [ ] Enable Remote Control API plugin
- [ ] Enable Remote Control Web Interface plugin
- [ ] Enable Pixel Streaming plugin
- [ ] Create Remote Control Presets
- [ ] Configure web server ports
- [ ] Test local connections

### Production
- [ ] Copy RemoteControlWebInterface/WebApp to package
- [ ] Set up dedicated signaling server
- [ ] Configure TURN server for mobile/secure networks
- [ ] Set up HTTPS/WSS for production
- [ ] Configure firewall rules (ports 7000, 8888, 80)
- [ ] Load balance multiple UE5 instances

## 7. Code Examples

### Control UE5 from Python (AI Server)

```python
import requests
import json

class UE5RemoteControl:
    def __init__(self, host="localhost", port=7000):
        self.base_url = f"http://{host}:{port}/remote"
    
    def get_presets(self):
        response = requests.get(f"{self.base_url}/presets")
        return response.json()
    
    def set_property(self, preset, property_name, value):
        return requests.put(
            f"{self.base_url}/object/property",
            json={
                "PresetName": preset,
                "PropertyName": property_name,
                "PropertyValue": value
            }
        ).json()
    
    def execute_function(self, preset, function_name, params={}):
        return requests.post(
            f"{self.base_url}/object/call",
            json={
                "PresetName": preset,
                "FunctionName": function_name,
                "Parameters": params
            }
        ).json()

# Usage
ue5 = UE5RemoteControl()
ue5.set_property("MainPreset", "CameraActor.FOV", 90)
ue5.execute_function("MainPreset", "SpawnActor", {"ActorClass": "Cube"})
```

### WebSocket Integration

```python
import asyncio
import websockets

async def stream_ue5_events():
    uri = "ws://localhost:7000/remote/events"
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            print(f"UE5 Event: {data}")
            # Process event, trigger AI response, etc.
```

## 8. Troubleshooting

### Remote Control API Issues

**Problem:** Can't connect to port 7000
- **Solution:** Check Project Settings → Plugins → Remote Control → Enable Web Server

**Problem:** Properties not updating
- **Solution:** Ensure properties are exposed in Remote Control Preset

### Pixel Streaming Issues

**Problem:** "WebRTC negotiated" but no video
- **Solution:** Check firewall, ensure signaling server is running

**Problem:** High latency
- **Solution:** Reduce resolution, increase frame rate, use hardware encoding

**Problem:** Mobile devices can't connect
- **Solution:** Set up TURN server for NAT traversal

### Web Interface Issues

**Problem:** Web UI not loading
- **Solution:** Copy WebApp folder to packaged game directory

**Problem:** Multiple clients out of sync
- **Solution:** Check WebSocket connection, ensure all clients connect to same server

## 9. Performance Optimization

### Pixel Streaming
- Use H.264 hardware encoding (NVENC/QuickSync)
- Target 30-60 FPS for smooth experience
- Adaptive bitrate based on network
- Resolution: 1920x1080 recommended, 1280x720 for mobile

### Remote Control API
- Batch property updates when possible
- Use WebSocket events instead of polling
- Cache preset information

## 10. Security Considerations

### Production Deployment
- Enable HTTPS/WSS (not HTTP/WS)
- Use authentication tokens
- Whitelist allowed IP addresses
- Rate limit API requests
- Don't expose development ports publicly

### Remote Control API
```python
# Add authentication to requests
headers = {"Authorization": f"Bearer {API_TOKEN}"}
requests.get(f"{UE5_URL}/remote/presets", headers=headers)
```

## Resources

- [Remote Control API Documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/remote-control-api-for-unreal-engine)
- [Remote Control Web Interface Guide](https://dev.epicgames.com/documentation/en-us/unreal-engine/remote-control-web-application-for-unreal-engine)
- [Pixel Streaming Documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/pixel-streaming-in-unreal-engine)
- [WebUI Plugin](https://github.com/tracerinteractive/UnrealWebUI)
- [WebUI Vue Framework](https://github.com/u4yk/WebUIVue)
