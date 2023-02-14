

from typing import List, Dict
import os
from CustomEntityExtractor.NumberEntityExtractor import NumberEntityExtractor
from DataManager.constants import RANGE_ENTITY_LABEL
from Parser.DataParser import DataParser
from Parser.DataWriter import DataWriter
from Parser.RasaCommunicator import RasaCommunicator
from Parser.QuestionAnswer import QuestionAnswer
from Parser.DataLoader import DataLoader
from Data_Ingestion.SparseMatrix import SparseMatrix

from actions.entititesHelper import filterEntities

import aiohttp
import asyncio

class ParserFacade():
    def __init__(self, dataLoader, dataWriter ):
        
        self.dataLoader : DataLoader = dataLoader
        self.dataWriter : DataWriter = dataWriter
        self.rasaCommunicator : RasaCommunicator = RasaCommunicator()
        self.numberEntityExtractor = NumberEntityExtractor()
        self.parser = DataParser()
        self.entityConfidenceKey = "confidence_entity"
        self.confidenceThreshold = 0.5
        self.state = "idle"

        #To support when we want to use a different parser for a particular section
        # self.parsers = {
        #                 "basis for selection": tempParser, 
        #                 "freshman profile_percentile": CDSDataParser("freshman profile_percentile",  self.dataWriter)

        #                 }

    async def parse(self):
        sectionFullNames : List[str] = self.dataLoader.getAllSectionDataFullName()
        sectionToData : Dict[str, List[any]] = dict()
        sectionToMetadata : Dict[str, List[any]] = dict()

        async with aiohttp.ClientSession() as session:
            tasks = []
           
            for sectionFullName in sectionFullNames:
                # if not section in self.parsers.keys():
                #     continue
                print("PARSING", sectionFullName)
                questionAnswers : List[QuestionAnswer] = self.dataLoader.getQuestionsAnswerForSection(sectionFullName)
                for questionAnswer in questionAnswers:
                    if questionAnswer.isMetaData: 
                        #Lets store metadata seperately
                        # questionAnswer.setEntities([questionAnswer.question])
                        continue
                    else:
                        # response : Dict
                        task = asyncio.create_task(self.rasaCommunicator.parseMessage(questionAnswer.getQuestion(), session=session))
                        tasks.append(task)

            responses = await asyncio.gather(*tasks)
            # print(responses)
          
            
            index = 0
            for sectionFullName in sectionFullNames:
                questionAnswers : List[QuestionAnswer] = self.dataLoader.getQuestionsAnswerForSection(sectionFullName)
                sectionAndSubSection = sectionFullName.split("_")
                section = sectionAndSubSection[0]
                subSection = sectionAndSubSection[len(sectionAndSubSection)-1]
                
                for questionAnswer in questionAnswers:
                    if questionAnswer.isMetaData: 
                        continue
                    numberEntities = self.numberEntityExtractor.extractEntities(questionAnswer.getQuestion())
                    response = responses[index]
                    entities = response["entities"] + numberEntities
                    highConfidenceEntities = []

                    #Filter out entities with low confidence
                    # for entity in entities:
                    #     if self.entityConfidenceKey in entity.keys():
                    #         if entity[self.entityConfidenceKey] >= self.confidenceThreshold:
                    #             highConfidenceEntities.append(entity)
                    #     else: 
                    #         highConfidenceEntities.append(entity)

                    highConfidenceEntities = self.removeLowConfidenceEntities(entities)
                    entityValues = []
                    for entity in highConfidenceEntities:
                        entityValues.append(entity["value"])
                    questionAnswer.setEntities(entityValues)

                    index = index + 1

                # Parsed data is sparse matrix, it can be extended to support other types as well.
                parsedData = self.parser.parse(subSection, questionAnswers) 
                if section in sectionToData:
                    sectionToData[section].append(parsedData)
                else: 
                    sectionToData[section] = [parsedData]

            # sparseMatrices.append(sparseMatrix)
        # might want to refactor so it doesn't assume sparse matrix
        self.write(sectionToData)
        
    def removeLowConfidenceEntities(self,entities):
        highConfidenceEntities = []
        for entity in entities:
            if self.entityConfidenceKey in entity.keys():
                if entity[self.entityConfidenceKey] >= self.confidenceThreshold:
                    highConfidenceEntities.append(entity)
                else: 
                    highConfidenceEntities.append(entity)
        return highConfidenceEntities
        
    def write(self,sectionToData):
        self.dataWriter.write(sectionToData)

        



    
     
        
       
    
    
    
