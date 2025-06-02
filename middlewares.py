from abc import ABC, abstractmethod
from .message import HMPMessage

class Middleware(ABC):
    @abstractmethod
    def pre_execute(self, message: HMPMessage) -> HMPMessage:
        pass

    @abstractmethod
    def post_execute(self, original: HMPMessage, result: HMPMessage) -> HMPMessage:
        pass

class LoggingMiddleware(Middleware):
    def pre_execute(self, message: HMPMessage) -> HMPMessage:
        print(f"[LOG-PRE] Agent={message.agent} Payload={message.payload}")
        return message

    def post_execute(self, original: HMPMessage, result: HMPMessage) -> HMPMessage:
        print(f"[LOG-POST] Agent={result.agent} Result={result.payload}")
        return result
