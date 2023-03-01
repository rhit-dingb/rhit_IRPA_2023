from typing import List
from Parser.RasaCommunicator import RasaCommunicator
from Data_Ingestion.SubsectionQnA import SubsectionQnA
from Data_Ingestion.MongoProcessor import MongoProcessor
from Data_Ingestion.TopicData import TopicData
from Parser.SparseMatrixDataParser import SparseMatrixDataParser


class ConvertToSparseMatrixDecorator():
    def __init__(self, decorated):
        #probably will use an more abstract class.
        self.decorated : MongoProcessor = decorated 
        self.rasaCommunicator = RasaCommunicator()
        self.sparseMatrixDataParser = SparseMatrixDataParser()


    from typing import List
from Parser.ParserFacade import ParserFacade
from Parser.QuestionAnswer import QuestionAnswer
from Parser.RasaCommunicator import RasaCommunicator
from Data_Ingestion.SubsectionQnA import SubsectionQnA
from Data_Ingestion.MongoProcessor import MongoProcessor
from Data_Ingestion.TopicData import TopicData
from Parser.SparseMatrixDataParser import SparseMatrixDataParser


class ConvertToSparseMatrixDecorator():
    def __init__(self, decorated):
        #probably will use an more abstract class.
        self.decorated : MongoProcessor = decorated 
        self.rasaCommunicator = RasaCommunicator()
        self.sparseMatrixDataParser = SparseMatrixDataParser()
        self.parserFacade : ParserFacade = ParserFacade(None, None, None)


    async def getDataByDbNameAndIntent(self, client, intent, dbName) -> TopicData:
        topicData = TopicData(intent)
        subsectionQnAList : List[SubsectionQnA] = await self.decorated.getDataByDbNameAndIntent(client, intent, dbName)
        for subsectionQnA in subsectionQnAList:
            questionAnswerDataModels = []
            questionAnswersRaw = subsectionQnA.questionAnswers
            # print("_____")
            # print(questionAnswersRaw)
            for questionKey in questionAnswersRaw:
                answer = questionAnswersRaw[questionKey]
                questionAns = QuestionAnswer(questionKey, answer, [], False)
                questionAnswerDataModels.append(questionAns)
            
            responses = await self.rasaCommunicator.parseMessagesAsync(questionAnswersRaw.keys())
            # might move this function to rasa communicator
            numQuestionParsed= self.parserFacade.setEntitiesForQuestionAndAnswer(questionAnswerDataModels, responses, 0 )
            sparseMatrix = self.sparseMatrixDataParser.parse(subsectionQnA.subSectionName,questionAnswerDataModels)
            sparseMatrix.metadata = subsectionQnA.metadata
            topicData.addSparseMatrix(subsectionQnA.subSectionName, sparseMatrix)
        
        return topicData
         


            


         

