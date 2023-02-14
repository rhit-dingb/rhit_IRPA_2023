from typing import Dict, List
from Knowledgebase.ShouldAddRowInterface import ShouldAddRowInterface
from Data_Ingestion.constants import OPERATION_ALLOWED_COLUMN_VALUE
from actions.entititesHelper import removeDuplicatedEntities
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

class FuzzyShouldAddRowStrategy(ShouldAddRowInterface):
    def __init__(self):
        super().__init__()
        self.vectorizer : TfidfVectorizer = None
        self.similarityThreshold = 0.3
        

    def determineShouldAddRow(self, row, entities : List[Dict], sparseMatrix):
        # Note: we only want to consider entities that are supported by this sparse matrix, so we can answer the user's question as best as possible
        #DUPLICATED CODE, need to move
        filteredEntities = []
        columns = row.index
        processedColumn =  [str(c).lower() for c in columns]

        # filter out entity that is not in sparse matrix columns
        for entity in entities:
            entityValue = entity["value"]
            if entityValue.lower() in processedColumn:
                filteredEntities.append(entity)
        uniqueEntities = removeDuplicatedEntities(filteredEntities)
        uniqueEntityValuesFound = [e["value"] for e in uniqueEntities]
        self.initializeTfidf(sparseMatrix)
        res = self.shouldUseOrNot(row, uniqueEntityValuesFound)
        if res == True:
            return uniqueEntities
        else: 
            return []
        

    def shouldUseOrNot(self,row, uniqueEntityValues):
        entityString = " ".join(uniqueEntityValues)
        rowString = self.convertRowToString(row)
        entityStringVec = self.vectorizer.transform([entityString])
        rowStringVec = self.vectorizer.transform([rowString])

        # print(entityStringVec)
        # print(rowStringVec)
        sim = cosine_similarity(entityStringVec, rowStringVec)
        print("SIMILARITY")
        print(sim[0][0])
        print(rowString)
        if sim[0][0] >= self.similarityThreshold:
           
            return True
        else:
            return False
     



    def convertRowToString(self, row):
        document = []
        for column in row.index:
            if row[column] == 1:
                document.append(column)
            
        return " ".join(document)

    def initializeTfidf(self, sparseMatrix):
        if self.vectorizer == None:
            self.vectorizer = TfidfVectorizer()
            documents = []
            for row in sparseMatrix:
                documentString = self.convertRowToString(row)
                documents.append(documentString)
            
            print(documents)
            self.vectorizer.fit_transform(documents)