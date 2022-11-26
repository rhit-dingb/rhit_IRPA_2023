import os
from Parser.ParserFacade import ParserFacade
from Parser.CDSDataLoader import CDSDataLoader
from Parser.ExcelSparseMatrixDataWriter import ExcelSparseMatrixDataWriter

def main():
    print(os.listdir("./"))
    
    #Write to 2020-2021 cds data excel file for now.
    writePath = "./CDSData/CDS_SPARSE_2020_2021.xlsx"
    dataLoader = CDSDataLoader()
    dataLoader.loadData("./NewCDSDataFromClient/CDSQuestionAnswer_2020_2021.xlsx")
    dataWriter = ExcelSparseMatrixDataWriter(writePath)
    parserFacade = ParserFacade(dataLoader=dataLoader, dataWriter=dataWriter)
    parserFacade.parse(2020)
    

if __name__ == "__main__":
    main()
        