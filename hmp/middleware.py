from .agent_base import Middleware

class LoggingMiddleware(Middleware):
    def pre_execute(self, message):
        print(f"[LOG-PRE] In: Agent={message.agent}, PayloadItems={len(message.payload)}, ContextKeys={list(message.context.keys())}")
        return message

    def post_execute(self, original, result):
        print(f"[LOG-POST] Out: OriginalAgent={original.agent}, ResultAgent={result.agent}, ResultPayloadItems={len(result.payload)}, ResultContextKeys={list(result.context.keys())}")
        return result
