from typing import List
from Parser.RasaCommunicator import RasaCommunicator
from Data_Ingestion.SubsectionQnA import SubsectionQnA
from Data_Ingestion.MongoProcessor import MongoProcessor
from Data_Ingestion.TopicData import TopicData
from Parser.SparseMatrixDataParser import SparseMatrixDataParser


from typing import List
from Parser.ParserFacade import ParserFacade
from Parser.QuestionAnswer import QuestionAnswer
from Parser.RasaCommunicator import RasaCommunicator
from Data_Ingestion.SubsectionQnA import SubsectionQnA
from Data_Ingestion.MongoProcessor import MongoProcessor
from Data_Ingestion.TopicData import TopicData
from Parser.SparseMatrixDataParser import SparseMatrixDataParser

from collections import defaultdict

class ConvertToSparseMatrixDecorator():
    def __init__(self, decorated):
        #probably will use an more abstract class.
        self.decorated : MongoProcessor = decorated 
        self.rasaCommunicator = RasaCommunicator()
        self.sparseMatrixDataParser = SparseMatrixDataParser()
        self.parserFacade : ParserFacade = ParserFacade(None, None, None)


    async def getDataByDbNameAndSection(self, client, section, dbName) -> TopicData:
        topicData = TopicData(section)
        subsectionQnAList : List[SubsectionQnA] = await self.decorated.getDataByDbNameAndSection(client, section, dbName)
        questionsToParse = []
        subsectionToQuestionAnswerDataModels = dict()
        for subsectionQnA in subsectionQnAList:
            subsectionToQuestionAnswerDataModels[subsectionQnA.subSectionName] = []

        for subsectionQnA in subsectionQnAList:
            questionAnswersRaw = subsectionQnA.questionAnswers
            for questionKey in questionAnswersRaw:
                answer = questionAnswersRaw[questionKey]
                questionAns = QuestionAnswer(questionKey, answer, [], False)
                subsectionToQuestionAnswerDataModels[subsectionQnA.subSectionName].append(questionAns)

            questionsToParse = questionsToParse + list(questionAnswersRaw.keys())
            # responses = await self.rasaCommunicator.parseMessagesAsync(questionAnswersRaw.keys())
            # might move this function to rasa communicator

        index = 0 
        responses = await self.rasaCommunicator.parseMessagesAsync(questionsToParse)
        for subsectionQnA in subsectionQnAList:
            subsectionName = subsectionQnA.subSectionName
            questionAnswers  = subsectionToQuestionAnswerDataModels[subsectionName]
            numQuestionParsed= self.parserFacade.setEntitiesForQuestionAndAnswer(questionAnswers, responses, index)
            sparseMatrix = self.sparseMatrixDataParser.parse(subsectionName, questionAnswers )
           
            sparseMatrix.metadata = subsectionQnA.metadata
            topicData.addSparseMatrix(subsectionQnA.subSectionName, sparseMatrix)
            index = index + numQuestionParsed
        
        return topicData
         


            


         

