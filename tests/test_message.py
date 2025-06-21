import hmp.message as message


def test_message_parse_and_encode():
    raw = 'test_agent|int:1,str:foo|k1=int:2;k2=str:bar'
    msg = message.HMPMessage(raw)
    assert msg.agent == 'test_agent'
    assert msg.payload == [1, 'foo']
    assert msg.context == {'k1': 2, 'k2': 'bar'}
    assert msg.encode() == raw
