
#This is a very basic implementation of parser that will parse the questions/answer from the client and convert to sparse matrix.
from typing import Dict, List, Tuple
from Parser.QuestionAnswer import QuestionAnswer
from Parser.DataWriter import DataWriter
from Data_Ingestion.SparseMatrix import SparseMatrix
from CustomEntityExtractor.NumberEntityExtractor import NumberEntityExtractor
from Parser.RasaCommunicator import RasaCommunicator

import pandas as pd
import aiohttp
import asyncio

from Parser.DataParser import DataParser



class SparseMatrixDataParser(DataParser):
    def __init__(self):
       pass

    def parseMetadata(self, metaDataQuestionAnswers : List[QuestionAnswer] ) -> Dict[str, str] :
        metadata = dict()
        for questionAnswer in metaDataQuestionAnswers:
            question = questionAnswer.getQuestion()
            answer = questionAnswer.getAnswer()
            if str(answer) == "nan":
                answer = ""
            metadata[question.lower()] = answer
            
        return metadata
    


       
    def parse(self, subsectionName : str , questionAnswers : List[QuestionAnswer]) -> SparseMatrix:
        # self.setEntitiesForQuestionAndAnswer(questionAnswers, responsesFromRasa)
        everyUniqueEntity = []
        matrixData = []
        sparseMatrix = None
        questionAnswersWithNoMetadata = list(filter(lambda quesAns: not quesAns.isMetaData, questionAnswers))
        metadataQuestionAnswer = list(filter(lambda quesAns: quesAns.isMetaData, questionAnswers))

        metadata : Dict[str, str] = self.parseMetadata(metadataQuestionAnswer)
        for questionAnswer in questionAnswersWithNoMetadata:
            # print(questionAnswer.entities)
            for entity in questionAnswer.entities:
                if entity in everyUniqueEntity:
                    continue
                else:
                    everyUniqueEntity.append(entity)

        for questionAnswer in questionAnswersWithNoMetadata:
            row = self.convertQuestionAnswerToRow(questionAnswer, everyUniqueEntity)
            matrixData.append(row)
        
        columns = ["Value"]
        columns = columns + everyUniqueEntity
        sparseMatrixDataFrame = pd.DataFrame(columns=columns, data = matrixData)
        questions = []

        for qa in questionAnswersWithNoMetadata:
            questions.append(qa.question)

        sparseMatrix = SparseMatrix(sparseMatrixDf=sparseMatrixDataFrame, subSectionName= subsectionName, questions=questions, metadata=metadata)
        return sparseMatrix
    
                    
    def convertQuestionAnswerToRow(self, questionAnswer : QuestionAnswer, allEntities : List[str]) -> List[str]:
        row = []
        row.append(questionAnswer.answer)
        entityFromRasaAfterParsingQuestion = questionAnswer.entities
        for entity in allEntities:
            if entity in entityFromRasaAfterParsingQuestion:
                row.append(1)
            else:
                row.append(0)
                
        return row
        
        
                    
                
        