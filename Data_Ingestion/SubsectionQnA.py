from typing import Dict


class SubsectionQnA():
    """
    Internal data model representing a subsection and all of its question and answer pairs, along with relevant metadata.
    """
    def __init__(self, subSectionName, questionAnswers, metadata):
        
        self.subSectionName = subSectionName
        self.metadata = metadata
        self.questionAnswers : Dict[str, str] = questionAnswers

    
    
        