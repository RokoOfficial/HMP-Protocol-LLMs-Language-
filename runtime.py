from typing import List
from .message import HMPMessage
from .typesystem import HMPTypeSystem
from .exceptions import HMPError

class HMPRuntime:
    def __init__(self, registry):
        self.registry = registry

    def execute(self, raw_hmp_string: str) -> HMPMessage:
        current_message = HMPMessage(raw_hmp_string)
        for mw in self.registry.middlewares:
            current_message = mw.pre_execute(current_message)
        agent = self.registry.get_agent(current_message.agent)
        result = agent.handle(current_message.payload, current_message.context)
        for mw in reversed(self.registry.middlewares):
            result = mw.post_execute(current_message, result)
        return result

    def batch_execute(self, hmp_lines: List[str]) -> List[HMPMessage]:
        results = []
        for line in hmp_lines:
            try:
                results.append(self.execute(line))
            except HMPError as e:
                error_payload = HMPTypeSystem.encode(f"Falha: {e}")
                fallback = HMPMessage(f"error_handler|{error_payload}|original_line=str:{line[:50]}")
                results.append(fallback)
            except Exception as e:
                error_payload = HMPTypeSystem.encode(f"Erro inesperado: {e}")
                fallback = HMPMessage(f"error_handler|{error_payload}|original_line=str:{line[:50]}")
                results.append(fallback)
        return results
