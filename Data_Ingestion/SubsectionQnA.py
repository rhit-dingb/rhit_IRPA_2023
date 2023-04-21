from typing import Dict


class SubsectionQnA():
    def __init__(self, subSectionName, questionAnswers, metadata):
        self.subSectionName = subSectionName
        self.metadata = metadata
        self.questionAnswers : Dict[str, str] = questionAnswers

    
    
        