from prompt import Prompt


class BotResponse:
    def __init__(self, model,created_at,message: Prompt):
        self.model = model
        self.created_at = created_at
        self.message = message
