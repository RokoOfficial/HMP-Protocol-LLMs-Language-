"""
HMP Framework - Hybrid Messaging Protocol

A modular framework for computational agents oriented by structured messages.

Author: RokoOfficial
Version: 1.0
License: Apache 2.0
"""

from .core import HMPMessage, HMPRuntime, HMPTypeSystem, HMPError
from .agents import BaseAgent, AgentRegistry, ShellAgent, RESTAgent, DataPipeAgent, MLModelAgent
from .middleware import Middleware
from .plugins import PluginManager

__version__ = '1.0.0'
__author__ = 'RokoOfficial'
__license__ = 'Apache 2.0'

__all__ = [
    'HMPMessage',
    'HMPRuntime',
    'HMPTypeSystem',
    'HMPError',
    'BaseAgent',
    'AgentRegistry',
    'ShellAgent',
    'RESTAgent',
    'DataPipeAgent',
    'MLModelAgent',
    'Middleware',
    'PluginManager',
]
