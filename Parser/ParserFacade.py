

from typing import List, Dict
import os
from Parser.CDSDataParser import CDSDataParser
from Parser.SparseMatrixDataWriter import SparseMatrixDataWriter
from Parser.RasaCommunicator import RasaCommunicator
from Parser.QuestionAnswer import QuestionAnswer
from Parser.JsonCDSDataLoader import JsonCDSDataLoader
from Parser.ExcelSparseMatrixDataWriter import ExcelSparseMatrixDataWriter
from Parser.CDSDataLoader import CDSDataLoader

class ParserFacade():
    def __init__(self, dataLoader, dataWriter):
        self.dataLoader : CDSDataLoader = dataLoader
        self.dataWriter : SparseMatrixDataWriter = dataWriter
        self.rasaCommunicator : RasaCommunicator = RasaCommunicator()
        
        
        #Im using one parser for now, later we probably want to have a list of parser, one for each section(including subsections)
        tempParser = CDSDataParser("basis for selection",  self.dataWriter)
        self.parsers = {"basis for selection": tempParser }
       
        

    def parse(self):
       sections : List[str] = self.dataLoader.getAllSections()
       for section in sections:
            questionAnswers : List[QuestionAnswer] = self.dataLoader.getQuestionsAnswerForSection(section)
            for questionAnswer in questionAnswers:
                response : Dict = self.rasaCommunicator.parseMessage(questionAnswer.getQuestion())
                entityValues = []
                for entity in response["entities"]:
                    entityValues.append(entity["value"])
        
                questionAnswer.setEntities(entityValues)
                
            if section in self.parsers: 
                parser : CDSDataParser = self.parsers[section]
                parser.parseQuestionAnswerToSparseMatrix(questionAnswers) 
            
        



    
     
        
       
    
    
    
