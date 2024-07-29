import json
class Prompt:
    def __init__(self,role,content):
        self.role = role
        self.content = content

    def to_json(self):
        return dict(role=self.role,content=self.content)

