
import unittest
from Parser.JsonDataLoader import JsonDataLoader
from Parser.MongoDbNoChangeDataWriter import MongoDbNoChangeDataWriter

from Parser.NoChangeDataParser import NoChangeDataParser
from Parser.ParserFacade import ParserFacade
import json
import os 
class test_input_data_parser(unittest.TestCase):
    def setUp(self):
        print(os.listdir("."))
        f = open('./tests/testMaterials/parserData/JsonInputExcelData.json')
        data = json.load(f)
        f.close()
        self.jsonCdsLoader = JsonDataLoader()
        self.jsonCdsLoader.loadData(data)
        self.dataParser = NoChangeDataParser()
        self.dataWriter = MongoDbNoChangeDataWriter("test_file")
        self.parserFacade = ParserFacade(dataLoader=self.jsonCdsLoader, dataWriter=self.dataWriter, dataParser=self.dataParser)

    def test_(self):
        pass


    

