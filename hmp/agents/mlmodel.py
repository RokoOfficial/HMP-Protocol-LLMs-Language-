"""
MLModel Agent - Simulate machine learning model inference.

Author: RokoOfficial
License: MIT
"""

from typing import Any, Dict, List
from ..core.message import HMPMessage
from ..core.typesystem import HMPTypeSystem
from .base import BaseAgent


class MLModelAgent(BaseAgent):
    """Agent for simulating ML model inference."""
    
    def __init__(self, model_path: str):
        """Initialize with a model path."""
        self.model_path = model_path
        self.model_repr = {"path": model_path, "status": "simulado"}

    def handle(self, payload: List[Any], context: Dict[str, Any]) -> HMPMessage:
        """Run simulated inference on input data."""
        if not payload:
            return HMPMessage(
                f"mlmodel|{HMPTypeSystem.encode('Sem dados de entrada.')}|error=str:sem_payload"
            )
            
        try:
            # Simulate output based on hash of input
            sim_output = float(abs(hash(str(payload))) % 1000) / 10.0
            return HMPMessage(
                f"mlmodel|{HMPTypeSystem.encode(sim_output)}|model_path=str:{self.model_path}"
            )
        except Exception as e:
            return HMPMessage(
                f"mlmodel|{HMPTypeSystem.encode(str(e))}|error=str:erro_modelo"
            )
