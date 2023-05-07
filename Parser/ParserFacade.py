

from typing import List, Dict
import os
from CustomEntityExtractor.NumberEntityExtractor import NumberEntityExtractor
from DataManager.constants import RANGE_ENTITY_LABEL
from Parser.SparseMatrixDataParser import SparseMatrixDataParser
from Parser.DataWriter import DataWriter
from Parser.RasaCommunicator import RasaCommunicator
from Parser.QuestionAnswer import QuestionAnswer
from Parser.DataLoader import DataLoader
from Data_Ingestion.SparseMatrix import SparseMatrix

from actions.entititesHelper import filterEntities
from actions.entititesHelper import removeLowConfidenceEntities


from Parser import DataParser



class ParserFacade():

    """
    Class that server as a facade to use DataLoader, DataWriter and DataParser together.
    """
    def __init__(self, dataLoader, dataWriter, dataParser ):
        
        self.dataLoader : DataLoader = dataLoader
        self.dataWriter : DataWriter = dataWriter
        self.dataParser : DataParser = dataParser
        self.rasaCommunicator : RasaCommunicator = RasaCommunicator()
        self.numberEntityExtractor = NumberEntityExtractor()
        self.state = "idle"



    async def parse(self):
        sectionFullNames : List[str] = self.dataLoader.getAllSectionDataFullName()
        sectionToData : Dict[str, List[any]] = dict()
    
        questions = []
        responses = []
        for sectionFullName in sectionFullNames:
            # if not section in self.parsers.keys():
            #     continue
            questionAnswers : List[QuestionAnswer] = self.dataLoader.getQuestionsAnswerForSectionAndSubsection(sectionFullName)
            for questionAnswer in questionAnswers:
                if questionAnswer.isMetaData: 
                    continue
                else:
                    questions.append(questionAnswer.getQuestion())
        
        # responses = await self.rasaCommunicator.parseMessagesAsync(questions)
        
        index = 0
        for sectionFullName in sectionFullNames:
            questionAnswers : List[QuestionAnswer] = self.dataLoader.getQuestionsAnswerForSectionAndSubsection(sectionFullName)
            sectionAndSubSection = sectionFullName.split("_")
            section = sectionAndSubSection[0]
            subSection = sectionAndSubSection[len(sectionAndSubSection)-1]

            # numQuestionSet = self.setEntitiesForQuestionAndAnswer(questionAnswers, responses, index)

            parsedData = self.dataParser.parse(subSection, questionAnswers) 
            if section in sectionToData:
                sectionToData[section].append(parsedData)
            else: 
                sectionToData[section] = [parsedData]

            # if section in sectionToData:
            #     sectionToData[section][subSection] = questionAnswers
            # else: 
            #     sectionToData[section] = dict()
            #     sectionToData[section][subSection] = questionAnswers

            # index = index + numQuestionSet
        self.write(sectionToData)
        
 
    def setEntitiesForQuestionAndAnswer(self,questionAnswers : List[QuestionAnswer], responses :Dict[any, any], startIndex  ):
        count = startIndex
        for questionAnswer in questionAnswers:
            if questionAnswer.isMetaData: 
                continue
            numberEntities = self.numberEntityExtractor.extractEntities(questionAnswer.getQuestion())
            response = responses[count]
            entities = response["entities"] + numberEntities
            highConfidenceEntities = []

            highConfidenceEntities = removeLowConfidenceEntities(entities)
            entityValues = []
            for entity in highConfidenceEntities:
                entityValues.append(entity["value"])
            questionAnswer.setEntities(entityValues)
            count = count + 1

        return count - startIndex



    def write(self,sectionToData):
        
        self.dataWriter.write(sectionToData)

        



    
     
        
       
    
    
    
