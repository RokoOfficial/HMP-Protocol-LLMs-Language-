import json
import base64
from datetime import datetime
from typing import Any
from .exceptions import HMPError

class HMPTypeSystem:
    TYPES = {
        'int': lambda v: int(v, 0),
        'float': float,
        'str': str,
        'bool': lambda v: v.lower() in {'true', '1', 'yes', 'y'},
        'json': json.loads,
        'bin': base64.b64decode,
        'dt': lambda v: datetime.fromisoformat(v.replace("Z", "+00:00"))
    }

    @classmethod
    def parse(cls, item: str) -> Any:
        if ':' not in item:
            try:
                return int(item)
            except ValueError:
                try:
                    return float(item)
                except ValueError as e:
                    raise HMPError(f"Valor sem prefixo inválido: {item!r}") from e

        prefix, value = item.split(":", 1)
        try:
            parser = cls.TYPES.get(prefix)
            if not parser:
                raise HMPError(f"Prefixo desconhecido: {prefix!r}")
            return parser(value)
        except Exception as e:
            raise HMPError(f"Falha ao decodificar {prefix}:{value!r}") from e

    @classmethod
    def encode(cls, val: Any) -> str:
        if isinstance(val, bool):
            return f"bool:{str(val).lower()}"
        if isinstance(val, int):
            return f"int:{val}"
        if isinstance(val, float):
            return f"float:{val}"
        if isinstance(val, str):
            return f"str:{val.replace('|', '|||')}"
        if isinstance(val, bytes):
            return f"bin:{base64.b64encode(val).decode()}"
        if isinstance(val, datetime):
            return f"dt:{val.isoformat()}"
        return f"json:{json.dumps(val, separators=(',', ':'))}"

def tokenize_hmp(payload_str: str):
    tokens = []
    buffer = []
    depth = 0
    in_quotes = False
    i = 0
    while i < len(payload_str):
        ch = payload_str[i]
        if ch == ',' and depth == 0 and not in_quotes:
            token = ''.join(buffer).strip()
            if token:
                tokens.append(token)
            buffer.clear()
        else:
            if ch in '[{':
                depth += 1
            elif ch in ']}':
                depth -= 1
            buffer.append(ch)
        i += 1
    last_token = ''.join(buffer).strip()
    if last_token:
        tokens.append(last_token)
    return tokens
