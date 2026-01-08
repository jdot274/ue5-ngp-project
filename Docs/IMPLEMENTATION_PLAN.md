# UE5-NGP AI Assistant - Implementation Plan

## Project Overview

Transform ue5-ngp-project into an AI-assisted UE5 app builder with:
- **External web interface** running outside UE5  
- **Real-time viewport streaming** via WebRTC/WebSocket
- **Natural language AI control** using LLMs
- **Automated NGP pipeline** with smart optimization
- **Remote Blueprint generation**

---

## System Architecture

```
[Web Browser Interface] 
         ↕ WebSocket/WebRTC
[Python AI Server (MCP/LLM)]
         ↕ TCP Socket 
[Unreal Engine 5 + Plugin]
```

**Key Principle**: The interface is **EXTERNAL** - you control and view UE5 remotely from a web browser.

---

## Phase 1: Core Infrastructure

### 1.1 Project Structure
```
ue5-ngp-project/
├── WebInterface/       # Next.js web dashboard
├── AIServer/          # Python orchestration server
├── Plugins/           
│   ├── UE5RemoteControl/  # C++ remote control plugin
│   └── NGPPipeline/       # Enhanced NGP integration
└── Docs/              # Documentation
```

### 1.2 AI Server Setup (Python)
**File**: `AIServer/server.py`

Key components:
- FastAPI web framework
- WebSocket server for bidirectional communication  
- MCP bridge for Claude/GPT integration
- Video stream processor
- Command router to UE5

### 1.3 Web Interface (Next.js)
**Directory**: `WebInterface/`

Features:
- Live UE5 viewport streaming player
- Chat interface for natural language commands
- Visual pipeline designer
- Asset browser
- Performance monitor

---

## Phase 2: Remote Viewing

### 2.1 Viewport Streaming Options

**Option A: WebRTC (Recommended)**
```
UE5 PixelStreaming → WebRTC → Browser
- Latency: 50-100ms
- Interactive (mouse/keyboard input)
- Highest quality
```

**Option B: WebSocket JPEG**
```
UE5 Capture → JPEG encode → WebSocket → Browser Canvas
- Latency: 200-500ms  
- Simpler implementation
- Good for monitoring
```

### 2.2 UE5 Plugin Implementation
**Plugin**: `Plugins/UE5RemoteControl/`

**Components**:
1. TCP Server (Port 9000) - Receives commands
2. Viewport Capturer - Streams video
3. State Broadcaster - Publishes events
4. Blueprint API - Remote Blueprint control

---

## Phase 3: AI Integration

### 3.1 MCP Bridge
**File**: `AIServer/mcp_bridge/server.py`

Connects to:
- Claude (Anthropic)
- GPT-4 (OpenAI)
- Local LLMs (Ollama)

Translates natural language → UE5 Python commands

### 3.2 Example Commands

```
User: "Import yesterday's NGP rock scan"
AI: Executes multi-step workflow:
    1. Find NGP output files
    2. Convert to USD format  
    3. Import to UE5
    4. Apply materials
    5. Enable Nanite

User: "Create a Blueprint that rotates this actor"
AI: Generates Blueprint:
    1. Create new Blueprint class
    2. Add rotation logic nodes
    3. Connect execution pins
    4. Compile Blueprint
```

---

## Phase 4: NGP Pipeline Automation

### 4.1 AI-Powered Optimization
- Analyze capture quality
- Suggest optimal NGP parameters
- Automated material mapping
- Smart LOD generation
- Performance optimization

### 4.2 Workflow Engine
**File**: `AIServer/workflows/engine.py`

Features:
- Multi-step operation orchestration
- Progress tracking & status updates
- Error recovery & retry logic
- Parallel task execution

---

## Implementation Checklist

### Documentation
- [x] Implementation Plan (this file)
- [ ] Architecture Diagram
- [ ] API Reference
- [ ] Setup Guide
- [ ] User Manual

### AI Server (Python)
- [ ] `AIServer/requirements.txt`
- [ ] `AIServer/server.py`  
- [ ] `AIServer/mcp_bridge/server.py`
- [ ] `AIServer/websocket/server.py`
- [ ] `AIServer/streaming/processor.py`
- [ ] `AIServer/workflows/engine.py`
- [ ] `AIServer/config.py`

### Web Interface (Next.js)
- [ ] `WebInterface/package.json`
- [ ] `WebInterface/components/UnrealViewport.jsx`
- [ ] `WebInterface/components/CommandChat.jsx`
- [ ] `WebInterface/components/PipelineDesigner.jsx`
- [ ] `WebInterface/lib/websocket.ts`
- [ ] `WebInterface/lib/ue5-client.ts`

### UE5 Plugin (C++)
- [ ] `Plugins/UE5RemoteControl/UE5RemoteControl.uplugin`
- [ ] `Source/RemoteExecution/RemoteExecutionModule.h`
- [ ] `Source/ViewportCapture/ViewportCapture.h`  
- [ ] `Source/StateBroadcaster/StateBroadcaster.h`
- [ ] `Source/BlueprintAPI/BlueprintGenerator.h`

### Examples & Config
- [ ] `Examples/basic_commands.py`
- [ ] `Examples/ngp_workflow.py`
- [ ] `.env.example`
- [ ] `docker-compose.yml`

---

## Quick Start Guide

### 1. Clone Repository
```bash
git clone https://github.com/jdot274/ue5-ngp-project
cd ue5-ngp-project
```

### 2. Start AI Server
```bash
cd AIServer
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python server.py
```

### 3. Start Web Interface
```bash
cd WebInterface
npm install
npm run dev
# Open http://localhost:3000
```

### 4. Install UE5 Plugin
```bash
cp -r Plugins/UE5RemoteControl /path/to/YourProject/Plugins/
# Enable in UE5: Edit > Plugins > UE5RemoteControl > Enable > Restart
```

### 5. Configure API Keys
```bash
cp .env.example .env
# Edit .env and add:
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```

### 6. Start Using
1. Launch UE5 with your project
2. Open web interface at localhost:3000
3. You should see UE5 viewport streaming
4. Type commands in chat: "Create a cube at 0,0,100"

---

## Technology Stack

**Web Interface**
- Next.js 14 (React framework)
- TailwindCSS (styling)
- Socket.io (WebSocket client)
- WebRTC API (video streaming)

**AI Server**  
- FastAPI (async Python web framework)
- python-socketio (WebSocket server)
- anthropic/openai SDKs (LLM APIs)
- aiortc (WebRTC Python)
- opencv-python (video processing)

**UE5 Plugin**
- C++ with Unreal Engine 5.4+
- Python Script Plugin
- Pixel Streaming Plugin  
- Json Utilities Module
- Networking Module

---

## MVP Features (Must Have)

1. ✅ Web interface with viewport viewer
2. ✅ WebSocket bidirectional communication
3. ✅ Basic command execution in UE5
4. ✅ Viewport streaming (JPEG over WebSocket)
5. ✅ MCP integration with Claude/GPT

## V2 Features (Should Have)

6. WebRTC streaming (better quality)
7. Blueprint generation from text
8. NGP workflow automation
9. Multi-user support
10. Performance monitoring

## Future Features (Nice to Have)

11. Voice commands
12. Mobile app (iOS/Android)
13. Cloud UE5 instances
14. Collaborative editing
15. Plugin marketplace

---

## Next Steps

After setup, you'll be able to:

✅ Control UE5 from web browser  
✅ View viewport in real-time  
✅ Execute AI-generated commands  
✅ Automate NGP → UE5 workflows  
✅ Generate Blueprints from descriptions  

**Start building with:** `npm run dev` and `python server.py`

See `Docs/` for detailed documentation.
