from Parser.SparseMatrixDataWriter import SparseMatrixDataWriter
from typing import List
from Data_Ingestion.SparseMatrix import SparseMatrix


import pandas as pd
from openpyxl import load_workbook

class ExcelSparseMatrixDataWriter(SparseMatrixDataWriter):
    def __init__(self, excelPath):
        # super().__init__()
        self.excelPath = excelPath
        self.excelWorkbook = load_workbook(self.excelPath)
        
    
    
    def writeSparseMatrix(self, sparseMatrix : SparseMatrix) -> None:
        df = sparseMatrix.getSparseMatrixDf()
        print(df)
        writer = pd.ExcelWriter(self.excelPath, engine = 'openpyxl')
        writer.book = self.excelWorkbook
        df.to_excel(writer, sheet_name = sparseMatrix.subSectionName, index=False)
        # writer.save()
        writer.close()

    
