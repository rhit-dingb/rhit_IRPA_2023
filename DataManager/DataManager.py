
from DataManager.YearDataSelector import YearlyDataSelector

"""
"Abstract" class to abstract sub classes responsible for retrieving sparse matrix to be searched
 given intent and entities containing year information.
 
There probably will be two implementation of this class one is for excel and another one for database.
"""
class DataManager():
    def __init__(self):
        self.dataSelector = YearlyDataSelector()

    """
    This is an abstract method.
    Given intent, start year and end year(i.e. 2020, 2021) of CDS data, it will look in the CDS data according to the year and 
    inside the CDS year, retreive the list of sparse matrices of the topic represented by the given intent.

    intent: intent of the user interpreted by rasa
    start: start year of the cds data we want
    end: end year of the cds data we want.

    return: a list of sparse matrices corresponding to the given intent. Each matrix is reprsented by pandas dataframe.
    """
    def getSparseMatricesByStartEndYearAndIntent(self, intent, start, end):
        raise Exception("This method should be override by a concrete class")


    """
    Given intent and entities, this function will determine the specific sparse matrix to be searched by the knowledgebase's search algorithm
    
    intent: intent of the user interpreted by rasa
    entities: list entities extracted by rasa. Each element in the list is a python dictionary. For example:
    {'entity': 'year', 'start': 58, 'end': 62, 'confidence_entity': 0.997698962688446, 'role': 'to', 'confidence_role': 0.7497242093086243, 'value': '2022', 'extractor': 'DIETClassifier'}

    return: a tuple of three elements, the first elem is the selected sparse matrix to search, the second elem is the start year and the third is the end year. 
    The year values is the what year CDS data was used.

    """
    def determineMatrixToSearch(self, intent, entities):
        sparseMatrices, startYear, endYear = self.dataSelector.selectDataToSearchByYear(self, intent, entities)
        selectedSparseMatrix = self.determineBestMatchingMatrix(sparseMatrices, entities)
        return (selectedSparseMatrix, startYear, endYear)


    """
    This function will determine which sparse matrix under an intent should we search based on the given entities.
    For each sparse matrix, it will calculate the number of entities that the sparse matrix has corresponding columns for.
    Then this function will find and return sparse matrix with the highest match number.
    We do this because for example, for enrollment, there are two matrix, one for general enrollment info and one for enrollment by race
    and if the user asks something like "how many hispanics male student are enrolled?" Should we use the general matrix that has gender
    or should we use the enrollment by race that has information on hispanic student enrollment?  
    If enrollment by race matrix has information about hispanic male enrollment, this algorithm would choose that. But in this cause,
    there is no such information and it is out of scope, so we can use any matrix, it will return 0 anywas.

    For now, we will always use the last matrix if there is a tie.
    """
    def determineBestMatchingMatrix(self, sparseMatrices, entities,):

        #print(sparseMatrices)
        maxMatch = []
        currMax = 0
        for sparseMatrix in sparseMatrices:
            entitiesMatchCount = 0
            for entity in entities:
                if entity["value"] in sparseMatrix.columns:
                    entitiesMatchCount = entitiesMatchCount+1
                    
            if entitiesMatchCount>currMax:
                maxMatch = []
                maxMatch.append(sparseMatrix)
                currMax = entitiesMatchCount
            elif entitiesMatchCount == currMax:
                maxMatch.append(sparseMatrix)


        return maxMatch[len(maxMatch)-1]



    """
    This function will get the most recent year of the data that is currently available. For example:
    if there are 2019-2020 data and 2020-2021 data, it will return a tuple: (2020, 2021)
    This function serves as the fallback. If the user didn't specify a year in their query, we will use the most recent year.
    """
    def getMostRecentYearRange():
        raise Exception("This method should be override by a concrete class")