import json


class ChatbotAnswer():
    """
    Chatbot answers data model for all knowledge
    """
    def __init__(self, answer, source, metadata = dict()):
        self.answer = answer
        self.source =source
        self.metadata = metadata

    def as_dict(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__))
