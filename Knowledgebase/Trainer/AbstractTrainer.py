
from typing import Dict, List, Tuple

from abc import ABC, abstractmethod

from Knowledgebase.DataModels.MultiFeedbackLabel import MultiFeedbackLabel


class AbstractTrainer(ABC) :
    """
    Class for trainer of various knowledgebase to inherit from.
    """
    def __init__(self):
        pass
    
    def filterTrainingLabelForSource(self, trainingLabels : List[MultiFeedbackLabel], source : str):
        """
        
        """
        filteredTrainingLabel = []
        for container in trainingLabels:
                fitleredFeedbackLabels = []
                for singleFeedbackLabel in container.feedbackLabels:
                    # print("FEEDBACK SOURCE VS CURRENT SOURCE")
                    # print(singleFeedbackLabel.source)
                    # print(source)
                    if singleFeedbackLabel.source == source:
                       
                        fitleredFeedbackLabels.append(singleFeedbackLabel)
                        print("ADDING", singleFeedbackLabel.answerProvided)

                if len(fitleredFeedbackLabels) > 0:
                    newMultiFeedbackLabel = MultiFeedbackLabel(container.query, fitleredFeedbackLabels)
              
                    filteredTrainingLabel.append(newMultiFeedbackLabel)

        return filteredTrainingLabel