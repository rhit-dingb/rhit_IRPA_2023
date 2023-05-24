from typing import Dict, List

from Data_Ingestion.constants import OPERATION_ALLOWED_COLUMN_VALUE
from Knowledgebase.SparseMatrixKnowledgebase.ShouldAddRowStrategy import ShouldAddRowStrategy
from actions.entititesHelper import removeDuplicatedEntities

class DefaultShouldAddRowStrategy(ShouldAddRowStrategy):
    """
    Default strategy which uses boolean search to determine whether a row of a sparse matrix should be used in the final answer when searching.
    
    """

    def __init__(self):
        super().__init__()
  
    def determineShouldAddRow(self, row, entities : List[Dict], sparseMatrix):    
        """
        Given a row in the sparse matrix and a list of entities, this function implementation 
        will check each entity to see if the column value for that entity is 1. If all the entity's corresponding
        column value is 1, it will return true, otherwise false.
        row: current row of sparse matrix in question -- a row in the pandas dataframe
        entities: list of entity, as python dictionaries
        """
        temp_count = 0

        # Note: we only want to consider entities that are supported by this sparse matrix, so we can answer the user's question as best as possible
        filteredEntities = []
        columns = row.index
        processedColumn =  [str(c).lower() for c in columns]

        # filter out entity that is not in sparse matrix columns
        for entity in entities:
            entityValue = entity["value"]
            if entityValue.lower() in processedColumn:
                filteredEntities.append(entity)

        uniqueEntities = removeDuplicatedEntities(filteredEntities)
    
        #uniqueEntityValuesFound = [e["value"].lower() for e in uniqueEntities]

        
        finalEntities = []
        for entity in uniqueEntities:
            if entity["value"] in processedColumn:
                finalEntities.append(entity)

        finalEntityValues = [e["value"].lower() for e in finalEntities]
        for entityValue in finalEntityValues:
           
            if entityValue in processedColumn and row[entityValue] == 1:
                # print("MATCHING")
                # print(entityValue)
                temp_count = temp_count+1
            else:
                print("MISMATCH AT", entityValue)
                continue
    
        if temp_count == len(finalEntityValues):
            # print("ACCEPT ROW")
            # print(row)
           # print("RETUNRING")
            #print(uniqueEntities)
            return finalEntities
        else:
            return []
