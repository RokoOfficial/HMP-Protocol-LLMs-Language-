import subprocess
import json
import requests
from typing import Any, Dict, List
from .message import HMPMessage
from .typesystem import HMPTypeSystem
from .agent_base import BaseAgent
from datetime import datetime

class ShellAgent(BaseAgent):
    MAX_OUTPUT = 1000
    def handle(self, payload: List[Any], context: Dict[str, Any]) -> HMPMessage:
        if not payload or not isinstance(payload[0], str):
            return HMPMessage(f"shell|{HMPTypeSystem.encode('Comando inválido.')}|{self._format_context_dict({'error': 'payload_format'})}")

        cmd = payload[0]
        timeout_val = float(context.get("timeout", 5.0))
        cwd_val = context.get("cwd")
        try:
            proc = subprocess.run(
                cmd, shell=True, capture_output=True, text=True,
                timeout=timeout_val, cwd=cwd_val if isinstance(cwd_val, str) else None
            )
            out = proc.stderr if proc.returncode != 0 else proc.stdout
            if len(out) > self.MAX_OUTPUT:
                out = out[:self.MAX_OUTPUT] + "..."
            return HMPMessage(f"shell|{HMPTypeSystem.encode(out.strip())}|code=int:{proc.returncode}")
        except Exception as e:
            return HMPMessage(f"shell|{HMPTypeSystem.encode(str(e))}|error=str:exec_error")

class RESTAgent(BaseAgent):
    def handle(self, payload: List[Any], context: Dict[str, Any]) -> HMPMessage:
        if len(payload) < 2:
            return HMPMessage(f"rest|{HMPTypeSystem.encode('Payload inválido')}|error=str:payload_short")
        method, url = payload[0], payload[1]
        data = payload[2] if len(payload) > 2 else None
        headers = context.get("headers", {})
        try:
            resp = requests.request(method, url, json=data if isinstance(data, (dict, list)) else None,
                                    data=data if isinstance(data, str) else None,
                                    headers=headers, timeout=10)
            if 'application/json' in resp.headers.get('Content-Type', ''):
                body = HMPTypeSystem.encode(resp.json())
            else:
                body = HMPTypeSystem.encode(resp.text)
            return HMPMessage(f"rest|{body}|status=int:{resp.status_code}")
        except Exception as e:
            return HMPMessage(f"rest|{HMPTypeSystem.encode(str(e))}|error=str:req_fail")

class DataPipeAgent(BaseAgent):
    def handle(self, payload: List[Any], context: Dict[str, Any]) -> HMPMessage:
        if len(payload) < 3:
            return HMPMessage(f"datapipe|{HMPTypeSystem.encode('Payload inválido.')}|error=str:payload_format")
        source, transform, destination = payload[:3]
        msg = f"Dados de '{source}' via '{transform}' para '{destination}' processados."
        return HMPMessage(f"datapipe|{HMPTypeSystem.encode(msg)}|status=str:ok")

class MLModelAgent(BaseAgent):
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model_repr = {"path": model_path, "status": "simulado"}

    def handle(self, payload: List[Any], context: Dict[str, Any]) -> HMPMessage:
        if not payload:
            return HMPMessage(f"mlmodel|{HMPTypeSystem.encode('Sem dados de entrada.')}|error=str:sem_payload")
        try:
            sim_output = float(abs(hash(str(payload))) % 1000) / 10.0
            return HMPMessage(f"mlmodel|{HMPTypeSystem.encode(sim_output)}|model_path=str:{self.model_path}")
        except Exception as e:
            return HMPMessage(f"mlmodel|{HMPTypeSystem.encode(str(e))}|error=str:erro_modelo")
