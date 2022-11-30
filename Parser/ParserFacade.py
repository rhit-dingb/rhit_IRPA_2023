

from typing import List, Dict
import os
from Parser.CDSDataParser import CDSDataParser
from Parser.SparseMatrixDataWriter import SparseMatrixDataWriter
from Parser.RasaCommunicator import RasaCommunicator
from Parser.QuestionAnswer import QuestionAnswer
from Parser.CDSDataLoader import CDSDataLoader
from Parser.ExcelSparseMatrixDataWriter import ExcelSparseMatrixDataWriter

class ParserFacade():
    def __init__(self, dataLoader, dataWriter):
        self.dataLoader : CDSDataLoader = dataLoader
        self.dataWriter : SparseMatrixDataWriter = dataWriter
        self.rasaCommunicator : RasaCommunicator = RasaCommunicator()
        
        
        #Im using one parser for now, later we probably want to have a list of parser, one for each section(including subsections)
        tempParser = CDSDataParser("basis for selection",  self.dataWriter)

        #To support when we want to use a different parser for a particular section
        self.parsers = {
                        # "basis for selection": tempParser, 
                        "freshman profile_percentile": CDSDataParser("freshman profile_percentile",  self.dataWriter)
                        }
       
        

    def parse(self, year : int):
       sections : List[str] = self.dataLoader.getAllSections()
       for section in sections:
            if not section in self.parsers.keys():
                continue
            questionAnswers : List[QuestionAnswer] = self.dataLoader.getQuestionsAnswerForSection(section)
            for questionAnswer in questionAnswers:
                response : Dict = self.rasaCommunicator.parseMessage(questionAnswer.getQuestion())
                entityValues = []
                for entity in response["entities"]:
                    entityValues.append(entity["value"])
        
                questionAnswer.setEntities(entityValues)
                
            if section in self.parsers.keys(): 
                parser : CDSDataParser = self.parsers[section]
                parser.parseQuestionAnswerToSparseMatrix(questionAnswers, year) 
            
        



    
     
        
       
    
    
    
