"""
DataPipe Agent - Simulate data pipeline processing.

Author: RokoOfficial
License: Apache 2.0
"""

from typing import Any, Dict, List
from ..core.message import HMPMessage
from ..core.typesystem import HMPTypeSystem
from .base import BaseAgent


class DataPipeAgent(BaseAgent):
    """Agent for simulating data pipeline flows between stages."""
    
    def handle(self, payload: List[Any], context: Dict[str, Any]) -> HMPMessage:
        """Process data through a pipeline."""
        if len(payload) < 3:
            return HMPMessage(
                f"datapipe|{HMPTypeSystem.encode('Payload inválido.')}|error=str:payload_format"
            )
            
        source, transform, destination = payload[:3]
        msg = f"Dados de '{source}' via '{transform}' para '{destination}' processados."
        return HMPMessage(f"datapipe|{HMPTypeSystem.encode(msg)}|status=str:ok")
