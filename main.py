import os
from CustomEntityExtractor.NumberEntityExtractor import NumberEntityExtractor
from Parser.MongoDBSparseMatrixDataWriter import MongoDBSparseMatrixDataWriter
from Parser.ParserFacade import ParserFacade
from Parser.CDSDataLoader import CDSDataLoader
from Parser.ExcelSparseMatrixDataWriter import ExcelSparseMatrixDataWriter

def main():
   
    #Write to 2020-2021 cds data excel file for now.
   
    dataLoader = CDSDataLoader("./NewCDSDataFromClient/CDSQuestionAnswer_2020_2021.xlsx")
    dataLoader.loadData()
    # writePath = "CDSSparse_test.xlsx"
    # dataWriter = ExcelSparseMatrixDataWriter(writePath)
    outputName = "CDS_2020_2021"
    dataWriter = MongoDBSparseMatrixDataWriter(outputName)
    parserFacade = ParserFacade(dataLoader=dataLoader, dataWriter=dataWriter)
    parserFacade.parse()
    
    
if __name__ == "__main__":
    main()
        