class A2AChannel:
    """
    Explicit Agent-to-Agent communication protocol.
    """

    def __init__(self):
        self.messages = {}

    def send(self, from_agent: str, to_agent: str, payload: dict):
        key = f"{from_agent} -> {to_agent}"
        self.messages[key] = payload

    def receive(self, from_agent: str, to_agent: str):
        key = f"{from_agent} -> {to_agent}"
        return self.messages.get(key, {})
