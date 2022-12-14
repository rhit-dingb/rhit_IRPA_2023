
from typing import Dict, Tuple
from DataManager.YearDataSelector import YearlyDataSelector
from DataManager.YearDataSelectorByCohort import YearlyDataSelectorByCohort
from Data_Ingestion.SparseMatrix import SparseMatrix
from Data_Ingestion.TopicData import TopicData
from Exceptions.ExceptionTypes import ExceptionTypes

from Exceptions.ExceptionMessages import NO_DATA_AVAILABLE_FOR_GIVEN_INTENT_FORMAT
from Exceptions.NoDataFoundException import NoDataFoundException
"""
"Abstract" class to abstract sub classes responsible for retrieving sparse matrix to be searched
 given intent and entities containing year information.
 
There probably will be two implementation of this class one is for excel and another one for database.
"""
class DataManager():
    def __init__(self):
        self.cohortYearDataSelector = YearlyDataSelectorByCohort()
        self.academicYearDataSelector = YearlyDataSelector()

    """
    This is an abstract method.
    Given intent, start year and end year(i.e. 2020, 2021) of CDS data, it will look in the CDS data according to the year and 
    inside the CDS year, retreive the list of sparse matrices of the topic represented by the given intent.

    intent: intent of the user interpreted by rasa
    start: start year of the cds data we want
    end: end year of the cds data we want.

    exceptionToThrow: the exception to throw if no data is found for the given year

    return: a list of sparse matrices corresponding to the given intent. Each matrix is reprsented by pandas dataframe.
    """
    def getSparseMatricesByStartEndYearAndIntent(self, intent, start, end, exceptionToThrow) -> TopicData:
        raise Exception("This method should be override by a concrete class")


    """
    Given intent and entities, this function will determine the specific sparse matrix to be searched by the knowledgebase's search algorithm
    
    intent: intent of the user interpreted by rasa
    entities: list entities extracted by rasa. Each element in the list is a python dictionary. For example:
    {'entity': 'year', 'start': 58, 'end': 62, 'confidence_entity': 0.997698962688446, 'role': 'to', 'confidence_role': 0.7497242093086243, 'value': '2022', 'extractor': 'DIETClassifier'}

    return: a tuple of three elements, the first elem is the selected sparse matrix to search, the second elem is the start year and the third is the end year. 
    The year values is the what year CDS data was used.

    """
    def determineMatrixToSearch(self, intent, entities) -> Tuple[SparseMatrix, str, str]: 
        sparseMatrices, startYear, endYear = self.cohortYearDataSelector.selectDataToSearchByYear(self, intent, entities)
        # print(sparseMatrices)
        if sparseMatrices == None:
            sparseMatrices, startYear, endYear = self.academicYearDataSelector.selectDataToSearchByYear(self, intent, entities)   
        
        
        errorMessage = NO_DATA_AVAILABLE_FOR_GIVEN_INTENT_FORMAT.format(topic = intent.replace("_", " "), start= startYear, end =endYear)
        selectedSparseMatrix = self.determineBestMatchingMatrix(sparseMatrices, entities, errorMessage)     
        return (selectedSparseMatrix, startYear, endYear)
       


    """
    This function will determine which sparse matrix under an intent should we search based on the given entities.

    First, it will check if any of the entity labels includes any subsections sparse matrix for the topic
    corresponding to the detected intent. For example, if an entity with race label was detected with enrollment intent, 
    it will tell TopicData for enrollemnt if it has a sparse matrix of the name "race"
    If there is one it will return it. Otherwise it will do the following:

    For each sparse matrix, it will calculate the number of entities that the sparse matrix has corresponding columns for.
    Then this function will find and return sparse matrix with the highest match number.
    We do this because for example, for enrollment, there are two matrix, one for general enrollment info and one for enrollment by race
    and if the user asks something like "how many hispanics male student are enrolled?" Should we use the general matrix that has gender
    or should we use the enrollment by race that has information on hispanic student enrollment?  

    If enrollment by race matrix has information about hispanic male enrollment, this algorithm would choose that. But in this case,
    there is no such information. so we can use any matrix. 

    However, if the user specify something like degree-seeking which is a column on both race and general enrollment matrix,
    we would want to use the genereal enrollment matrix but there will be a tie. So in this case, we use the first matrix for tie,
    which will be general enrollment. In the future, if this problem is encountered and we would want to use another matrix for tie,
    we can store a field in TopicData to indicate use which matrix as default in case of a tie.

    """
    def determineBestMatchingMatrix(self, topicData : TopicData, entities : Dict, errorMessage : str) ->  SparseMatrix:
        doesEntityMapToAnySubsections, sparseMatrixFound = topicData.doesEntityIncludeAnySubsections(entities)

        if doesEntityMapToAnySubsections:
            return sparseMatrixFound

        else:
            maxMatch = []
            currMax = 0
            sparseMatricesDictionary : Dict[SparseMatrix] = topicData.getSparseMatrices()
            for key in sparseMatricesDictionary.keys():

                sparseMatrix : SparseMatrix = sparseMatricesDictionary[key]
                
                entityValues = []
                for entity in entities:
                    entityValues.append(entity["value"])
                
                entitiesMatchCount : int  = sparseMatrix.determineEntityMatchToColumnCount(entityValues)
                if entitiesMatchCount>currMax:
                    maxMatch = []
                    maxMatch.append(sparseMatrix)
                    currMax = entitiesMatchCount
                elif entitiesMatchCount == currMax:
                    maxMatch.append(sparseMatrix)


        
            #raise an error if no best matching matrix is found
            if len(maxMatch) == 0:
                raise NoDataFoundException(errorMessage, ExceptionTypes.NoSparseMatrixDataAvailableForGivenIntent)
            
            return maxMatch[0]



    """
    This function will get the most recent year of the data that is currently available. For example:
    if there are 2019-2020 data and 2020-2021 data, it will return a tuple: (2020, 2021)
    This function serves as the fallback. If the user didn't specify a year in their query, we will use the most recent year.
    """
    def getMostRecentYearRange() -> Tuple[str, str]:
        raise Exception("This method should be override by a concrete class")