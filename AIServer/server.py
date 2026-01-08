# AI Server for UE5 NGP Project
# Provides AI assistance, code generation, and Blueprint creation

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import anthropic
import openai
import asyncio
import json
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="UE5 AI Assistant Server")

# CORS middleware for web interface
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Client connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"Client disconnected. Total connections: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

# Request/Response models
class BlueprintGenerationRequest(BaseModel):
    description: str
    blueprint_type: str  # Actor, Component, Widget, etc.
    context: Optional[Dict] = None

class CodeGenerationRequest(BaseModel):
    description: str
    language: str  # C++, Python, Blueprint
    context: Optional[Dict] = None

class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict] = None

# AI Integration
class AIService:
    def __init__(self):
        self.anthropic_client = None
        self.openai_client = None
        
    def initialize(self, anthropic_key: str = None, openai_key: str = None):
        if anthropic_key:
            self.anthropic_client = anthropic.Anthropic(api_key=anthropic_key)
        if openai_key:
            self.openai_client = openai.OpenAI(api_key=openai_key)
    
    async def generate_blueprint(self, request: BlueprintGenerationRequest) -> Dict:
        """Generate UE5 Blueprint code based on description"""
        prompt = f"""
You are an Unreal Engine 5 expert. Generate a Blueprint structure for:
Type: {request.blueprint_type}
Description: {request.description}

Provide the Blueprint as JSON with nodes, connections, and properties.
"""
        
        if self.anthropic_client:
            message = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}]
            )
            return {"blueprint": message.content[0].text, "provider": "anthropic"}
        
        return {"error": "No AI provider configured"}
    
    async def generate_code(self, request: CodeGenerationRequest) -> Dict:
        """Generate C++ or Python code for UE5"""
        prompt = f"""
You are an Unreal Engine 5 expert. Generate {request.language} code for:
Description: {request.description}

Provide clean, production-ready code with comments.
"""
        
        if self.anthropic_client:
            message = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}]
            )
            return {"code": message.content[0].text, "provider": "anthropic"}
        
        return {"error": "No AI provider configured"}
    
    async def chat(self, request: ChatRequest) -> Dict:
        """General AI chat assistance"""
        if self.anthropic_client:
            message = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4096,
                messages=[{"role": "user", "content": request.message}]
            )
            return {"response": message.content[0].text, "provider": "anthropic"}
        
        return {"error": "No AI provider configured"}

ai_service = AIService()

# API Endpoints
@app.get("/")
async def root():
    return {"status": "AI Server Running", "version": "1.0.0"}

@app.post("/api/blueprint/generate")
async def generate_blueprint(request: BlueprintGenerationRequest):
    try:
        result = await ai_service.generate_blueprint(request)
        return result
    except Exception as e:
        logger.error(f"Blueprint generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/code/generate")
async def generate_code(request: CodeGenerationRequest):
    try:
        result = await ai_service.generate_code(request)
        return result
    except Exception as e:
        logger.error(f"Code generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        result = await ai_service.chat(request)
        return result
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# WebSocket endpoint for real-time communication
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            if message.get("type") == "blueprint_request":
                request = BlueprintGenerationRequest(**message["data"])
                result = await ai_service.generate_blueprint(request)
                await websocket.send_json({"type": "blueprint_response", "data": result})
            
            elif message.get("type") == "code_request":
                request = CodeGenerationRequest(**message["data"])
                result = await ai_service.generate_code(request)
                await websocket.send_json({"type": "code_response", "data": result})
            
            elif message.get("type") == "chat":
                request = ChatRequest(**message["data"])
                result = await ai_service.chat(request)
                await websocket.send_json({"type": "chat_response", "data": result})
            
            # Broadcast to other connected clients
            await manager.broadcast({"type": "activity", "data": message})
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
