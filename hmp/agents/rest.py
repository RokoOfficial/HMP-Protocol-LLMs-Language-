"""
REST Agent - Make HTTP requests.

Author: RokoOfficial
License: MIT
"""

import requests
from typing import Any, Dict, List
from ..core.message import HMPMessage
from ..core.typesystem import HMPTypeSystem
from .base import BaseAgent


class RESTAgent(BaseAgent):
    """Agent for making HTTP/REST requests."""
    
    def handle(self, payload: List[Any], context: Dict[str, Any]) -> HMPMessage:
        """Make an HTTP request and return the response."""
        if len(payload) < 2:
            return HMPMessage(
                f"rest|{HMPTypeSystem.encode('Payload inválido')}|error=str:payload_short"
            )
            
        method, url = payload[0], payload[1]
        data = payload[2] if len(payload) > 2 else None
        headers = context.get("headers", {})
        
        try:
            resp = requests.request(
                method, 
                url, 
                json=data if isinstance(data, (dict, list)) else None,
                data=data if isinstance(data, str) else None,
                headers=headers, 
                timeout=10
            )
            
            if 'application/json' in resp.headers.get('Content-Type', ''):
                body = HMPTypeSystem.encode(resp.json())
            else:
                body = HMPTypeSystem.encode(resp.text)
                
            return HMPMessage(f"rest|{body}|status=int:{resp.status_code}")
        except Exception as e:
            return HMPMessage(
                f"rest|{HMPTypeSystem.encode(str(e))}|error=str:req_fail"
            )
