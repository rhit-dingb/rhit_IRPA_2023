import os
from Parser.ParserFacade import ParserFacade
from Parser.JsonCDSDataLoader import JsonCDSDataLoader
from Parser.ExcelSparseMatrixDataWriter import ExcelSparseMatrixDataWriter

def main():
    print(os.listdir("./"))
    
    #Write to 2020-2021 cds data excel file for now.
    filePath = "./CDSData/CDS_SPARSE_2020_2021.xlsx"
    dataLoader = JsonCDSDataLoader()
    dataWriter = ExcelSparseMatrixDataWriter(filePath)
    parserFacade = ParserFacade(dataLoader=dataLoader, dataWriter=dataWriter)
    parserFacade.parse()
    

if __name__ == "__main__":
    main()
        