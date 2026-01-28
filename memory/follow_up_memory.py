class FollowUpMemory:
    def __init__(self):
        self.preference = None
        self.strength = 0  # decay counter

    def update(self, user_input: str):
        """
        Capture explicit follow-up signals from user replies.
        """
        text = user_input.lower()

        if "example" in text:
            self.preference = "example"
            self.strength = 3
        elif "deeper" in text or "advanced" in text:
            self.preference = "deep"
            self.strength = 3
        elif "simple" in text:
            self.preference = "simple"
            self.strength = 3

    def decay(self):
        """
        Gradually forget preference if not reinforced.
        """
        if self.strength > 0:
            self.strength -= 1
        if self.strength == 0:
            self.preference = None

    def get_preference(self):
        return self.preference

    def store_from_response(self, response: str):
        """
        Observe assistant follow-up style to reinforce preference.
        """
        text = response.lower()
        if "example" in text:
            self.preference = "example"
            self.strength = 2
        elif "deeper" in text or "trade-off" in text:
            self.preference = "deep"
            self.strength = 2
