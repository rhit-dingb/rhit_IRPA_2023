from Knowledgebase.Knowledgebase import KnowledgeBase
from Data_Ingestion.ExcelProcessor import ExcelProcessor
import pandas as pd
import copy
import numpy as np

from Knowledgebase.Knowledgebase import KnowledgeBase
from Data_Ingestion.ExcelProcessor import ExcelProcessor
import copy
class SparseMatrixKnowledgeBase(KnowledgeBase):
    def __init__(self, filePath):
        self.excelProcessor = ExcelProcessor()
        self.topicToParse = ["General_Enrollment"]
        self.data = self.excelProcessor.processExcelSparse(filePath, self.topicToParse)
        self.m_df = self.data["General_Enrollment"] # this is HARD CODED NOW

    def searchForAnswer(self, intent, entities):
        count=0
        col_index=0
        #TODO filter out entities that are not under this intent

        for i in range(self.m_df['men'].size):
            temp_count = 0
            if self.m_df.loc[i,"total"] == 1:
                continue

            for entity in self.m_df.columns:
                if entity in entities: 
                    if self.m_df.loc[i,entity] == 1:
                        temp_count += 1
            if temp_count == len(entities):
                #print("Im ADDING " + str(self.m_df.loc[i,'Value']))
                count += self.m_df.loc[i,'Value']
                
        return str(count)

    def dummyRandomGeneratedDF(self):
        self.m_df = pd.DataFrame()
        self.m_df['Value'] = np.floor(np.random.uniform(low= 20, high=2000, size=(20,)))
        self.m_df['undergraduate'] = np.random.choice([0, 1], size=20, p=[.5, .5])
        self.m_df['grad'] = np.random.choice([0, 1], size=20, p=[.5, .5])
        self.m_df['male'] = np.random.choice([0, 1], size=20, p=[.8, .2])
        self.m_df['female'] = np.random.choice([0, 1], size=20, p=[.6, .4])
        self.m_df['degree-seeking'] = np.random.choice([0, 1], size=20, p=[.8, .2])
        self.m_df['non-degree-seeking'] = np.random.choice([0, 1], size=20, p=[.8, .2])
        self.m_df['full-time'] = np.random.choice([0, 1], size=20, p=[.8, .2])
        self.m_df['part-time'] = np.random.choice([0, 1], size=20, p=[.8, .2])
        self.m_df['freshman'] = np.random.choice([0, 1], size=20, p=[.8, .2])
        self.m_df['non-freshman'] = np.random.choice([0, 1], size=20, p=[.8, .2])
        self.m_df['first-year'] = np.random.choice([0, 1], size=20, p=[.7, .3])
        self.m_df['white'] = np.random.choice([0, 1], size=20, p=[.9, .1])
        self.m_df['african American'] = np.random.choice([0, 1], size=20, p=[.8, .2])
        self.m_df['asian'] = np.random.choice([0, 1], size=20, p=[.8, .2])
        self.m_df['hispanic'] = np.random.choice([0, 1], size=20, p=[.8, .2])
        self.m_df['pacific islander'] = np.random.choice([0, 1], size=20, p=[.8, .2])
        self.m_df['two or more races'] = np.random.choice([0, 1], size=20, p=[.9, .1])
        self.m_df['ethinicity unknown'] = np.random.choice([0, 1], size=20, p=[.6, .4])
        self.m_df['Total?'] = np.random.choice([0, 1], size=20, p=[.9, .1])


  
