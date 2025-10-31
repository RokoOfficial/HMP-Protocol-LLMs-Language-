"""
HMP Message - Core message class for HMP protocol.

Author: RokoOfficial
License: MIT
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List
from .exceptions import HMPError
from .typesystem import HMPTypeSystem, tokenize_hmp


@dataclass(frozen=True, slots=True)
class HMPMessage:
    """Immutable HMP message with agent, payload, and context."""
    raw: str
    agent: str = field(init=False)
    payload: List[Any] = field(init=False)
    context: Dict[str, Any] = field(init=False)

    def __post_init__(self) -> None:
        temp_raw_for_split = self.raw.replace("|||", "<HMP_PIPE_ESC>")
        parts = temp_raw_for_split.split("|", 2)

        if len(parts) < 2:
            raise HMPError("Mensagem HMP deve conter ao menos AGENTE e PAYLOAD, separados por '|'.")

        object.__setattr__(self, 'agent', parts[0].strip().replace("<HMP_PIPE_ESC>", "|"))

        payload_raw_str = parts[1].replace("<HMP_PIPE_ESC>", "|").strip()
        parsed_payload_items: List[Any] = []
        if payload_raw_str:
            payload_tokens = tokenize_hmp(payload_raw_str)
            for item_token in payload_tokens:
                try:
                    parsed_payload_items.append(HMPTypeSystem.parse(item_token))
                except HMPError as e:
                    raise HMPError(f"Falha ao processar item do payload HMP: {item_token!r}. Erro original: {e}")
        object.__setattr__(self, 'payload', parsed_payload_items)

        parsed_context: Dict[str, Any] = {}
        if len(parts) == 3 and parts[2].strip():
            context_raw_str = parts[2].strip()
            context_pairs = context_raw_str.split(";")
            for pair_str in context_pairs:
                if not pair_str.strip():
                    continue
                if "=" not in pair_str:
                    raise HMPError(f"Par de contexto malformado (esperado 'chave=valor'): {pair_str!r}")
                key_raw, value_raw = pair_str.split("=", 1)
                key = key_raw.strip().replace("<HMP_PIPE_ESC>", "|")
                value_str_for_parse = value_raw.strip().replace("<HMP_PIPE_ESC>", "|")
                try:
                    parsed_context[key] = HMPTypeSystem.parse(value_str_for_parse)
                except HMPError:
                    parsed_context[key] = value_str_for_parse
        object.__setattr__(self, 'context', parsed_context)

    def encode(self) -> str:
        """Encode the message back to HMP string format."""
        encoded_payload_items = [HMPTypeSystem.encode(v) for v in self.payload]
        payload_str = ",".join(encoded_payload_items)

        encoded_context_pairs = []
        for k, v in self.context.items():
            encoded_key_str = str(k).replace('|', '|||')
            encoded_value_str = HMPTypeSystem.encode(v)
            encoded_context_pairs.append(f"{encoded_key_str}={encoded_value_str}")
        context_str = ";".join(encoded_context_pairs)

        encoded_agent_str = self.agent.replace('|', '|||')
        return f"{encoded_agent_str}|{payload_str}|{context_str}"

    def __str__(self) -> str:
        """String representation of the message."""
        return self.encode()
