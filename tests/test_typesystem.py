import pytest
import hmp.typesystem as typesystem


def test_parse_encode_simple_types():
    assert typesystem.HMPTypeSystem.parse('int:5') == 5
    assert typesystem.HMPTypeSystem.encode(5) == 'int:5'
    assert typesystem.HMPTypeSystem.parse('float:1.5') == 1.5
    assert typesystem.HMPTypeSystem.encode(1.5) == 'float:1.5'
    assert typesystem.HMPTypeSystem.parse('str:abc') == 'abc'
    assert typesystem.HMPTypeSystem.encode('abc') == 'str:abc'


def test_tokenize_hmp():
    data = '1,{"a":2},[3,4],str:x'
    tokens = typesystem.tokenize_hmp(data)
    assert tokens == ['1', '{"a":2}', '[3,4]', 'str:x']
