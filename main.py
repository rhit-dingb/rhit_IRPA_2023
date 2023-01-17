import asyncio
import os
from CustomEntityExtractor.NumberEntityExtractor import NumberEntityExtractor
from Parser.MongoDBSparseMatrixDataWriter import MongoDBSparseMatrixDataWriter
from Parser.ParserFacade import ParserFacade
from Parser.DataLoader import DataLoader
from Parser.ExcelSparseMatrixDataWriter import ExcelSparseMatrixDataWriter
from Parser.ExcelCDSDataLoader import ExcelCDSDataLoader

async def main():
   
    #Write to 2020-2021 cds data excel file for now.
   
    dataLoader = ExcelCDSDataLoader("./NewCDSDataFromClient/CDSQuestionAnswer_2020_2021.xlsx")
    dataLoader.loadData()
    # writePath = "CDSSparse_test.xlsx"
    # dataWriter = ExcelSparseMatrixDataWriter(writePath)
    outputName = "CDS_2020_2021"
    dataWriter = MongoDBSparseMatrixDataWriter(outputName)
    parserFacade = ParserFacade(dataLoader=dataLoader, dataWriter=dataWriter)
    await parserFacade.parse()
    
    
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
        