

from typing import List, Dict
import os
from CustomEntityExtractor.NumberEntityExtractor import NumberEntityExtractor
from DataManager.constants import RANGE_ENTITY_LABEL
from Parser.DataParser import DataParser
from Parser.SparseMatrixDataWriter import SparseMatrixDataWriter
from Parser.RasaCommunicator import RasaCommunicator
from Parser.QuestionAnswer import QuestionAnswer
from Parser.DataLoader import DataLoader
from Parser.ExcelSparseMatrixDataWriter import ExcelSparseMatrixDataWriter
from Data_Ingestion.SparseMatrix import SparseMatrix

from actions.entititesHelper import filterEntities

import aiohttp
import asyncio

class ParserFacade():
    def __init__(self, dataLoader, dataWriter ):
        
        self.dataLoader : DataLoader = dataLoader
        self.dataWriter : SparseMatrixDataWriter = dataWriter
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
        sectionToSparseMatrices : Dict[str, List] = dict()
       

        async with aiohttp.ClientSession() as session:
            tasks = []
            for sectionFullName in sectionFullNames:
                # if not section in self.parsers.keys():
                #     continue
                print("PARSING", sectionFullName)
                questionAnswers : List[QuestionAnswer] = self.dataLoader.getQuestionsAnswerForSection(sectionFullName)
                for questionAnswer in questionAnswers:
                    # print(questionAnswer.question)
                    if questionAnswer.isMetaData: 
                        questionAnswer.setEntities([questionAnswer.question])
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
                    # if(section == "freshman profile"):
                    #     print(questionAnswer.question)
                    #     print(numberEntities)
                    # Filter out range entities
                    # entities = filterEntities(entities, [RANGE_ENTITY_LABEL])
                    highConfidenceEntities = []
                    #Filter out entities with low confidence
                    for entity in entities:
                        if self.entityConfidenceKey in entity.keys():
                            if entity[self.entityConfidenceKey] >= self.confidenceThreshold:
                                highConfidenceEntities.append(entity)
                        else: 
                            highConfidenceEntities.append(entity)
                    entityValues = []
                    for entity in highConfidenceEntities:
                        entityValues.append(entity["value"])
                    questionAnswer.setEntities(entityValues)

                    index = index + 1
                    
                sparseMatrix : SparseMatrix = self.parser.parseQuestionAnswerToSparseMatrix(subSection, questionAnswers) 
                if section in sectionToSparseMatrices:
                    sectionToSparseMatrices[section].append(sparseMatrix)
                else: 
                    sectionToSparseMatrices[section] = [sparseMatrix]

            # sparseMatrices.append(sparseMatrix)
        self.writeSparseMatrix(sectionToSparseMatrices)
           
        
        
    def writeSparseMatrix(self,sectionToSparseMatrices):
        self.dataWriter.writeSparseMatrices(sectionToSparseMatrices)

        



    
     
        
       
    
    
    
