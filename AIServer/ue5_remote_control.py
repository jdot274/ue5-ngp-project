"""UE5 Remote Control API Integration
Provides production-ready integration with Unreal Engine's Remote Control API.
"""

import requests
import websockets
import asyncio
import json
from typing import Dict, List, Any, Optional
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class UE5RemoteConfig:
    """Configuration for UE5 Remote Control connection"""
    host: str = "localhost"
    port: int = 7000
    protocol: str = "http"
    ws_protocol: str = "ws"
    timeout: int = 30
    
    @property
    def base_url(self) -> str:
        return f"{self.protocol}://{self.host}:{self.port}/remote"
    
    @property
    def ws_url(self) -> str:
        return f"{self.ws_protocol}://{self.host}:{self.port}/remote/events"


class UE5RemoteControlClient:
    """Production client for UE5 Remote Control API"""
    
    def __init__(self, config: Optional[UE5RemoteConfig] = None):
        self.config = config or UE5RemoteConfig()
        self.session = requests.Session()
        self.ws_connection = None
        self._event_handlers = []
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def close(self):
        """Close HTTP session"""
        self.session.close()
    
    # === Info Endpoints ===
    
    def get_server_info(self) -> Dict:
        """Get UE5 Remote Control server information"""
        response = self.session.get(
            f"{self.config.base_url}/info",
            timeout=self.config.timeout
        )
        response.raise_for_status()
        return response.json()
    
    def health_check(self) -> bool:
        """Check if UE5 Remote Control server is responsive"""
        try:
            info = self.get_server_info()
            return info.get("status") == "ok" or "version" in info
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    # === Preset Management ===
    
    def list_presets(self) -> List[Dict]:
        """Get all available Remote Control presets"""
        response = self.session.get(
            f"{self.config.base_url}/presets",
            timeout=self.config.timeout
        )
        response.raise_for_status()
        return response.json().get("Presets", [])
    
    def get_preset(self, preset_name: str) -> Dict:
        """Get detailed information about a specific preset"""
        response = self.session.get(
            f"{self.config.base_url}/preset/{preset_name}",
            timeout=self.config.timeout
        )
        response.raise_for_status()
        return response.json()
    
    def get_preset_properties(self, preset_name: str) -> List[Dict]:
        """Get all exposed properties in a preset"""
        preset = self.get_preset(preset_name)
        return preset.get("ExposedProperties", [])
    
    def get_preset_functions(self, preset_name: str) -> List[Dict]:
        """Get all exposed functions in a preset"""
        preset = self.get_preset(preset_name)
        return preset.get("ExposedFunctions", [])
    
    # === Property Control ===
    
    def set_property(self, 
                    preset_name: str,
                    property_name: str, 
                    value: Any,
                    generate_transaction: bool = True) -> Dict:
        """Set a property value in UE5
        
        Args:
            preset_name: Name of the Remote Control preset
            property_name: Path to the property (e.g., "Actor.Location.X")
            value: New value to set
            generate_transaction: Whether to generate undo/redo transaction
            
        Returns:
            Response from UE5
        """
        payload = {
            "objectPath": property_name,
            "propertyValue": value,
            "generateTransaction": generate_transaction
        }
        
        response = self.session.put(
            f"{self.config.base_url}/object/property",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=self.config.timeout
        )
        response.raise_for_status()
        return response.json()
    
    def get_property(self, preset_name: str, property_name: str) -> Any:
        """Get current property value from UE5"""
        payload = {
            "objectPath": property_name
        }
        
        response = self.session.put(
            f"{self.config.base_url}/object/property",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=self.config.timeout
        )
        response.raise_for_status()
        result = response.json()
        return result.get("value")
    
    def batch_set_properties(self, 
                            preset_name: str,
                            properties: Dict[str, Any]) -> List[Dict]:
        """Set multiple properties at once
        
        Args:
            preset_name: Name of the Remote Control preset
            properties: Dictionary of property_path: value pairs
            
        Returns:
            List of responses for each property
        """
        results = []
        for prop_path, value in properties.items():
            try:
                result = self.set_property(preset_name, prop_path, value)
                results.append({"property": prop_path, "success": True, "result": result})
            except Exception as e:
                results.append({"property": prop_path, "success": False, "error": str(e)})
                logger.error(f"Failed to set {prop_path}: {e}")
        return results
    
    # === Function Execution ===
    
    def call_function(self,
                     preset_name: str,
                     function_name: str,
                     parameters: Optional[Dict] = None,
                     generate_transaction: bool = False) -> Dict:
        """Call a Blueprint function in UE5
        
        Args:
            preset_name: Name of the Remote Control preset
            function_name: Name of the exposed function
            parameters: Function parameters as dictionary
            generate_transaction: Whether to generate undo/redo transaction
            
        Returns:
            Function execution result
        """
        payload = {
            "objectPath": function_name,
            "parameters": parameters or {},
            "generateTransaction": generate_transaction
        }
        
        response = self.session.put(
            f"{self.config.base_url}/object/call",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=self.config.timeout
        )
        response.raise_for_status()
        return response.json()
    
    # === Metadata Search ===
    
    def search_assets(self, 
                     class_name: Optional[str] = None,
                     package_path: Optional[str] = None,
                     object_name: Optional[str] = None) -> List[Dict]:
        """Search for assets in UE5 project
        
        Args:
            class_name: Filter by class (e.g., "StaticMesh", "Material")
            package_path: Filter by package path
            object_name: Filter by object name
            
        Returns:
            List of matching assets
        """
        params = {}
        if class_name:
            params["Class"] = class_name
        if package_path:
            params["PackagePath"] = package_path
        if object_name:
            params["ObjectName"] = object_name
        
        response = self.session.get(
            f"{self.config.base_url}/search/assets",
            params=params,
            timeout=self.config.timeout
        )
        response.raise_for_status()
        return response.json().get("Assets", [])
    
    def search_actors(self, actor_class: Optional[str] = None) -> List[Dict]:
        """Search for actors in current level
        
        Args:
            actor_class: Filter by actor class
            
        Returns:
            List of matching actors
        """
        params = {}
        if actor_class:
            params["Class"] = actor_class
        
        response = self.session.get(
            f"{self.config.base_url}/search/actors",
            params=params,
            timeout=self.config.timeout
        )
        response.raise_for_status()
        return response.json().get("Actors", [])
    
    # === WebSocket Event Streaming ===
    
    async def connect_events(self, 
                           event_handler=None):
        """Connect to WebSocket event stream
        
        Args:
            event_handler: Async callback function for events
        """
        if event_handler:
            self._event_handlers.append(event_handler)
        
        try:
            async with websockets.connect(self.config.ws_url) as websocket:
                self.ws_connection = websocket
                logger.info(f"Connected to UE5 events: {self.config.ws_url}")
                
                async for message in websocket:
                    try:
                        event_data = json.loads(message)
                        for handler in self._event_handlers:
                            await handler(event_data)
                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to parse event: {e}")
                    except Exception as e:
                        logger.error(f"Event handler error: {e}")
        except Exception as e:
            logger.error(f"WebSocket connection failed: {e}")
            raise
    
    def register_event_handler(self, handler):
        """Register an async event handler callback"""
        self._event_handlers.append(handler)
    
    # === Utility Methods ===
    
    def describe_object(self, object_path: str) -> Dict:
        """Get metadata about a UE5 object
        
        Args:
            object_path: Full path to object
            
        Returns:
            Object metadata including properties, functions, etc.
        """
        payload = {"objectPath": object_path}
        
        response = self.session.put(
            f"{self.config.base_url}/object/describe",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=self.config.timeout
        )
        response.raise_for_status()
        return response.json()
    
    def get_thumbnail(self, object_path: str) -> bytes:
        """Get thumbnail image for a UE5 asset
        
        Args:
            object_path: Full path to asset
            
        Returns:
            Thumbnail image as bytes
        """
        payload = {"objectPath": object_path}
        
        response = self.session.put(
            f"{self.config.base_url}/object/thumbnail",
            json=payload,
            timeout=self.config.timeout
        )
        response.raise_for_status()
        return response.content


# === Convenience Functions ===

def create_client(host: str = "localhost", 
                 port: int = 7000,
                 protocol: str = "http") -> UE5RemoteControlClient:
    """Create a configured UE5 Remote Control client
    
    Args:
        host: UE5 server hostname
        port: Remote Control API port (default 7000)
        protocol: http or https
        
    Returns:
        Configured client instance
    """
    config = UE5RemoteConfig(host=host, port=port, protocol=protocol)
    return UE5RemoteControlClient(config)


async def stream_ue5_events(host: str = "localhost",
                          port: int = 7000,
                          event_handler=None):
    """Stream real-time events from UE5
    
    Args:
        host: UE5 server hostname
        port: Remote Control API port
        event_handler: Async callback for events
    """
    config = UE5RemoteConfig(host=host, port=port)
    client = UE5RemoteControlClient(config)
    
    if event_handler:
        client.register_event_handler(event_handler)
    
    await client.connect_events()
