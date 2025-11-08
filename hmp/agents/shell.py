"""
Shell Agent - Execute shell commands safely.

Author: RokoOfficial
License: Apache 2.0
"""

import subprocess
from typing import Any, Dict, List
from ..core.message import HMPMessage
from ..core.typesystem import HMPTypeSystem
from .base import BaseAgent


class ShellAgent(BaseAgent):
    """Agent for executing shell commands with timeout and working directory support."""
    
    MAX_OUTPUT = 1000
    
    def handle(self, payload: List[Any], context: Dict[str, Any]) -> HMPMessage:
        """Execute a shell command and return the result."""
        if not payload or not isinstance(payload[0], str):
            return HMPMessage(
                f"shell|{HMPTypeSystem.encode('Comando inválido.')}|"
                f"{self._format_context_dict({'error': 'payload_format'})}"
            )

        cmd = payload[0]
        timeout_val = float(context.get("timeout", 5.0))
        cwd_val = context.get("cwd")
        
        try:
            proc = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=True, 
                text=True,
                timeout=timeout_val, 
                cwd=cwd_val if isinstance(cwd_val, str) else None
            )
            out = proc.stderr if proc.returncode != 0 else proc.stdout
            if len(out) > self.MAX_OUTPUT:
                out = out[:self.MAX_OUTPUT] + "..."
            return HMPMessage(
                f"shell|{HMPTypeSystem.encode(out.strip())}|code=int:{proc.returncode}"
            )
        except Exception as e:
            return HMPMessage(
                f"shell|{HMPTypeSystem.encode(str(e))}|error=str:exec_error"
            )
