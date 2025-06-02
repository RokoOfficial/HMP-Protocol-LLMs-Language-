from abc import ABC, abstractmethod
from typing import Any, Dict, List
from .typesystem import HMPTypeSystem

class Middleware(ABC):
    @abstractmethod
    def pre_execute(self, message):
        pass

    @abstractmethod
    def post_execute(self, original, result):
        pass

class BaseAgent(ABC):
    @abstractmethod
    def handle(self, payload: List[Any], context: Dict[str, Any]):
        pass

    def _format_context_dict(self, ctx: Dict[str, Any]) -> str:
        context_str_parts = []
        for k, v in ctx.items():
            encoded_k = str(k).replace('|', '|||')
            encoded_v = HMPTypeSystem.encode(v)
            context_str_parts.append(f"{encoded_k}={encoded_v}")
        return ";".join(context_str_parts)

class AgentRegistry:
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.middlewares: List[Middleware] = []

    def register_agent(self, name: str, agent: BaseAgent):
        self.agents[name] = agent

    def add_middleware(self, middleware: Middleware):
        self.middlewares.append(middleware)

    def get_agent(self, name: str) -> BaseAgent:
        agent = self.agents.get(name)
        if not agent:
            from .exceptions import HMPError
            raise HMPError(f"Agente não registrado: {name!r}")
        return agent
