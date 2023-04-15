from typing import Dict, List
from Knowledgebase.ShouldAddRowInterface import ShouldAddRowInterface
from Data_Ingestion.constants import OPERATION_ALLOWED_COLUMN_VALUE
from actions.entititesHelper import removeDuplicatedEntities
"""
Default strategy which uses boolean search to determine whether a row of a sparse matrix should be used in the total value while searching. More detail below
"""


class DefaultShouldAddRowStrategy(ShouldAddRowInterface):
    def __init__(self):
        super().__init__()
        
    """
    Given a row in the sparse matrix and a list of entities, this function implementation 
    will check each entity to see if the column value for that entity is 1. If all the entity's corresponding
    column value is 1, it will return true, otherwise false.
    row: current row of sparse matrix in question -- a row in the pandas dataframe
    entities: list of entity, as python dictionaries
    """

    def determineShouldAddRow(self, row, entities : List[Dict], sparseMatrix):
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
        uniqueEntityValuesFound = [e["value"].lower() for e in uniqueEntities]

        # for column in columns:
        #     print("CHECKING")
        #     print(column)
        #     if str(column).lower() in uniqueEntityValuesFound:
        #         if row[column] == 1:
        #             temp_count = temp_count + 1
        #     else:
        #         print("MISMATCH AT", column)
        # print(row)
        print("UNIQUE ENETITY VALUE FOUND", uniqueEntityValuesFound)
        for entityValue in uniqueEntityValuesFound:
            if entityValue in columns and row[entityValue] == 1:
                print("MATCHING")
                print(entityValue)
                temp_count = temp_count+1
            else:
                print("MISMATCH AT", entityValue)
                continue
        # print("MATCH")
        # print(temp_count)
        # print(len(uniqueEntities))
        if temp_count == len(uniqueEntities):
            # print("ACCEPT ROW")
            # print(row)
            return uniqueEntities
        else:
            return []
