import sys
from .exceptions import HMPError
from .typesystem import HMPTypeSystem, tokenize_hmp
from .message import HMPMessage
from .agent_base import BaseAgent, Middleware, AgentRegistry
from .agents import ShellAgent, RESTAgent, DataPipeAgent, MLModelAgent
from .middleware import LoggingMiddleware
from .plugin import PluginManager
from .runtime import HMPRuntime

# Provide an alias without hyphens for easier imports in external code and tests
sys.modules.setdefault('hmp', sys.modules[__name__])
