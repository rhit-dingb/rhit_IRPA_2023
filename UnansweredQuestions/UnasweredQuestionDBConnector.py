
from abc import ABC, abstractmethod
from typing import Dict, List
class UnansweredQuestionDbConnector(ABC):
    """
    Abstract class responsible for connection to the data source for unanswered question and their answers.
    """
   

    @abstractmethod
    def getAllUnansweredQuestionAndAnswer(self):
        """
        This method is responsible for retrieving all unanswered question and their answers if any.
        """
        pass

    @abstractmethod
    def getAnsweredQuestionSortedByDate(self,  order="ASCENDING"):
        """
        Get unanswered questions that are answered sorted by date
        :param order: The order to get the data. Options: ASCENDING, DESCENDING.
        """
        pass

    @abstractmethod
    def provideAnswerToUnansweredQuestion(questionId: str, answer: str):
        """
        This method is responsible for saving the answer for the unanswered question to the data source.
        :param questionId: The id for the unanswered question. 
        :param answer: The answer provide to the unanswered question
        """
        pass

    @abstractmethod
    def addNewUnansweredQuestion(question: str,  chatbotAnswers :  List[Dict[str, any]] ) -> str:
        """
        Add a new unanswered question to the data source along with the answers provided by the chatbot. If the unanswered question already exist,
        different policy to deal with this can be used such as: replace the old question, do nothing, add a duplicate copy. Currently we replace it in
        the MongoDbUnansweredQuestionConnector.
        :param question: The question that the user asked and is unanswered.
        :chatbotAnswers: List of chatbot answers provided to the user's question.
        Looks something like:
        [{'answer': 'Acceptance rate increased by 20%', 'source': 'unansweredQuestionEngine', 'metadata': {}, 'text': 'Acceptance rate increased by 20%', 'feedback': ''},

        {'answer': 'Students can be accepted for terms other than the fall with special permission.', 'source': 'QuestionAnswerKnowledgebase',
        
        'metadata': {'context': 'Students can be accepted for terms other than the fall with special permission.', 
        'offsets_in_document': [{'start': 0, 'end': 79, '__initialised__': True}], 
        'document_ids': ['c29b50dbae09be51f3a34444424bc81c'], 
        'actual answer': 'Students can be accepted for terms other than the fall with special permission.', 
        'document_content': 'Students can be accepted for terms other than the fall with special permission.', '
        document_question': 'are students accepted for terms other than the fall?'}, 
        'text': 'Students can be accepted for terms other than the fall with special permission.', 'feedback': ''}, 

        The main fields is the answer, and source, and the metadata can have various fields depending on the knowledgebase.

        :return: The unique id of the unanswered question that was added.
        """
        pass

    @abstractmethod
    def getQuestionAnswerObjectById(questionId : str):
        """
        Given a question id, return all the fields for that question
        """
        pass

    @abstractmethod
    def deleteUnansweredQuestion(questionId : str):
       """
       Given a question id, delete that unanswered question
       """
       pass


    @abstractmethod
    def updateFeedbackForAnswer(self, questionId : str, chatbotAnswer : str, feedback : str):
        """
        Update the feedback on a particular chatbot answer for that question.
        :param questionId: unanswered question id
        :param chatbotAnswer: A particular answer from the chatbot for the question it is associated with. This is the answer whose feedback should updated
        :param feedback: Feedback for the chatbot answer. The possible value is: "correct" and "incorrect".
        """
        pass

    @abstractmethod
    def updateTrainedStatus(self, questionId: str, status : bool):
        """
        Mark a unanswered question, denoting whether feedback on its chatbot answers have been used for training the knowledgebases.
        """
        pass
      
