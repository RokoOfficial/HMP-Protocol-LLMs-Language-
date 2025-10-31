"""
Base classes for HMP agents and registry.

Author: RokoOfficial
License: MIT
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List
from ..core.typesystem import HMPTypeSystem


class BaseAgent(ABC):
    """Base class for all HMP agents."""
    
    @abstractmethod
    def handle(self, payload: List[Any], context: Dict[str, Any]):
        """
        Handle a message payload with given context.
        
        Args:
            payload: List of parsed payload items
            context: Dictionary of context parameters
            
        Returns:
            HMPMessage with the result
        """
        pass

    def _format_context_dict(self, ctx: Dict[str, Any]) -> str:
        """Format a context dictionary for HMP encoding."""
        context_str_parts = []
        for k, v in ctx.items():
            encoded_k = str(k).replace('|', '|||')
            encoded_v = HMPTypeSystem.encode(v)
            context_str_parts.append(f"{encoded_k}={encoded_v}")
        return ";".join(context_str_parts)


class AgentRegistry:
    """Registry for managing agents and middlewares."""
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.middlewares: List = []

    def register_agent(self, name: str, agent: BaseAgent):
        """Register an agent with a given name."""
        self.agents[name] = agent

    def add_middleware(self, middleware):
        """Add a middleware to the processing pipeline."""
        self.middlewares.append(middleware)

    def get_agent(self, name: str) -> BaseAgent:
        """Get a registered agent by name."""
        agent = self.agents.get(name)
        if not agent:
            from ..core.exceptions import HMPError
            raise HMPError(f"Agente não registrado: {name!r}")
        return agent
