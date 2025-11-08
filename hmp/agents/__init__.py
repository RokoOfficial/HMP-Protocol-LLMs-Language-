"""
HMP Agents Module
Provides base classes and concrete agent implementations.

Author: RokoOfficial
License: Apache 2.0
"""

from .base import BaseAgent, AgentRegistry
from .shell import ShellAgent
from .rest import RESTAgent
from .datapipe import DataPipeAgent
from .mlmodel import MLModelAgent

__all__ = [
    'BaseAgent',
    'AgentRegistry',
    'ShellAgent',
    'RESTAgent',
    'DataPipeAgent',
    'MLModelAgent',
]
