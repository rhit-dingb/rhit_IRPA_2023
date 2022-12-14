
#This is a very basic implementation of parser that will parse the questions/answer from the client and convert to sparse matrix.
from typing import List
from Parser.QuestionAnswer import QuestionAnswer
from Parser.SparseMatrixDataWriter import SparseMatrixDataWriter
from Data_Ingestion.SparseMatrix import SparseMatrix
import pandas as pd

class CDSDataParser():
    def __init__(self,  sparseMatrixDataWriter : SparseMatrixDataWriter):
        self.sparseMatrixDataWriter = sparseMatrixDataWriter
       
    def parseQuestionAnswerToSparseMatrix(self,sectionName : str ,questionAnswers : QuestionAnswer, year: int) -> bool:
        everyUniqueEntity = []
        matrixData = []
        sparseMatrix = None
        
        for questionAnswer in questionAnswers:
            print(questionAnswer.entities)
            for entity in questionAnswer.entities:
            
                if entity in everyUniqueEntity:
                    continue
                else:
                    everyUniqueEntity.append(entity)
        for questionAnswer in questionAnswers:
            row = self.convertQuestionAnswerToRow(questionAnswer, everyUniqueEntity)
            matrixData.append(row)
        
        columns = ["Value"]
        columns = columns + everyUniqueEntity
        sparseMatrixDataFrame = pd.DataFrame(columns=columns, data = matrixData)
        sparseMatrix = SparseMatrix(sparseMatrixDf=sparseMatrixDataFrame, subSectionName= sectionName)
        self.sparseMatrixDataWriter.writeSparseMatrix(sparseMatrix)
                    
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
        
        
                    
                
        