from Parser.SparseMatrixDataWriter import SparseMatrixDataWriter
from typing import Dict, List
from Data_Ingestion.SparseMatrix import SparseMatrix


import pandas as pd
from openpyxl import load_workbook

# This writer currently only writes to existing excel file instead of creating one.
class ExcelSparseMatrixDataWriter(SparseMatrixDataWriter):
    def __init__(self, excelPath):
        self.excelPath = excelPath
        self.excelWorkbook = load_workbook(self.excelPath)
    
    
    def writeSparseMatrix(self, sparseMatrix : SparseMatrix, sectionName : str) -> None:
        df = sparseMatrix.getSparseMatrixDf()
        # print(df)
        writer = pd.ExcelWriter(self.excelPath, engine = 'openpyxl')
        writer.book = self.excelWorkbook
        sheetName = sectionName +"_"+sparseMatrix.subSectionName
        df.to_excel(writer, sheet_name = sheetName, index=False)
        # writer.save()
        writer.close()

    def writeSparseMatrices(self,  sectionToSparseMatrices : Dict[str, List[SparseMatrix]]) -> None:
        for section in sectionToSparseMatrices:
            sparseMatrices = sectionToSparseMatrices[section]
            for sparseMatrix in sparseMatrices:
                self.writeSparseMatrix(sparseMatrix, section)

    
