
from typing import List
import unittest
from Parser.JsonDataLoader import JsonDataLoader
from Parser.MongoDbNoChangeDataWriter import MongoDbNoChangeDataWriter
from Parser.SparseMatrixDataParser import SparseMatrixDataParser

from Parser.NoChangeDataParser import NoChangeDataParser
from Parser.ParserFacade import ParserFacade
import json
import os
from pymongo import MongoClient
from unittest.mock import MagicMock, patch, ANY
import asyncio
import DataManager.constants as constants
from Parser.QuestionAnswer import QuestionAnswer

class test_input_data_parser(unittest.TestCase):
    def setUp(self):
       
        f = open('./tests/testMaterials/parserData/JsonInputExcelData.json')
        self.data = json.load(f)
        f.close()
        self.jsonCdsLoader = JsonDataLoader()
        self.jsonCdsLoader.loadData(self.data)
        self.dataParser = NoChangeDataParser()
        with patch('pymongo.MongoClient') as mockDb:
            self.dataWriter = MongoDbNoChangeDataWriter("CDS_2020_2021", mockDb )
            self.mockDb = mockDb
        self.parserFacade = ParserFacade(dataLoader=self.jsonCdsLoader, dataWriter=self.dataWriter, dataParser=self.dataParser)

    def test_parse_input_excel_should_write_correct_data(self):
       
        asyncio.run(self.parserFacade.parse())
        sheetName = "Degree Conferred"
        expectedAnswer = self.getExpectedQuestionAnswers(sheetName)
        expectedAnswer[constants.DATABASE_SUBSECTION_FIELD_KEY] = sheetName.lower()
        # Can replace some of the complicated argument with ANY if we want.
        print(self.mockDb["CDS_2020_2021"])
        self.assertEqual(self.mockDb["CDS_2020_2021"][sheetName.lower()].update_one.called, True)
        # self.mockDb["CDS_2020_2021"][sheetName.lower()].update_one.assert_called_with({'subsection': sheetName.lower()}, {"$set":expectedAnswer}, upsert=True)
    
    def test_loader_get_question_answer_should_return_correct_data(self):
        jsonCdsLoader = JsonDataLoader()
        jsonCdsLoader.loadData(self.data)
        # sectionFullNames= jsonCdsLoader.getAllSectionDataFullName
        sectionFullName = "General Info"
        questionAnswersJson = self.data[sectionFullName]
        questionAnswers : List[QuestionAnswer]= jsonCdsLoader.getQuestionsAnswerForSection(sectionFullName.lower()) 
        
        self.assertEqual(questionAnswers[0].getQuestion().lower(), questionAnswersJson[0]["Question"].lower() )


    # Need to provide some question answer with fake entities, and see the resulting sparse matrix.
    # def test_sparse_matrix_data_parser_should_return_correct_sparse_matrix():
    #     dataParser = SparseMatrixDataParser()
    #     subsectionName : str , questionAnswers : List[QuestionAnswer]
    #     dataParser.parse()
    
    def getExpectedQuestionAnswers(self,name):
        questionAnswers = self.data[name]
        expectedAnswers = dict()
        expectedAnswers[constants.DATABASE_QUESTION_ANSWERS_KEY] = dict()
        isMetadata = False
        metadata = dict()
        for qa in questionAnswers:
            question = qa["Question"].lower()
            answer = qa["Answer"].lower()
            if question.lower() == "metadata":
                isMetadata = True
                continue

            if isMetadata:
                metadata[question] = answer
                continue

            expectedAnswers[constants.DATABASE_QUESTION_ANSWERS_KEY][question] = answer

        expectedAnswers[constants.DATABASE_METADATA_FIELD_KEY] = metadata
        return expectedAnswers

        





