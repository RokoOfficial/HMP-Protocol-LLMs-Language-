import hmp.agents as agents
import hmp.agent_base as agent_base
import hmp.runtime as runtime


def test_shell_agent_basic():
    registry = agent_base.AgentRegistry()
    registry.register_agent('shell', agents.ShellAgent())
    r = runtime.HMPRuntime(registry)
    result = r.execute('shell|str:echo test|')
    assert result.agent == 'shell'
    assert 'test' in result.payload[0]
