class MCPContext:
    def __init__(self, user_input: str):
        self.user_input = user_input
        self.memory = None
        self.signals = {}

    def attach_memory(self, memory):
        self.memory = memory

    def attach_signal(self, key: str, value):
        """
        Attach internal, silent signals for the LLM.
        These are NEVER user-facing.
        """
        if value is not None:
            self.signals[key] = value

    def export_for_llm(self) -> dict:
        """
        Export ONLY serializable data for CrewAI.
        """
        return {
            "user_input": self.user_input,
            "memory": self.memory,
            "signals": self.signals
        }
