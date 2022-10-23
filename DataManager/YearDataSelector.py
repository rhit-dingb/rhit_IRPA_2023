

"""
A class used to determine which CDS data to use given the year.
"""
from Exceptions.ExceptionMessages import NO_DATA_FOUND_FOR_ACADEMIC_YEAR_ERROR_MESSAGE_FORMAT
from Exceptions.ExceptionTypes import ExceptionTypes
from Exceptions.NoDataFoundException import NoDataFoundException


class YearlyDataSelector():
    """
    This function will get the specific sparse matrix that will be used based on the intent and entities that contains 
    information about year. Based on user input, the entities list will either have an year entity or it won't. If it does not,
    this function will retrieve and return the sparse matrices corresponding to the intent from the most recent CDS data.

    If the user does ask data specifically about year, there will be three cases we'll have to handle:
       1. The user specify the year with something like "2020-2021", then 2020-2021 will be extracted one entity. 
       This function use split by "-" to get the start and end year.
       2. If the user specify year saying: "from 2020 to 2021", 2020 and 2021 will be extracted as seperate entity and each will
       have role associated with them. In the case 2022 has role "from" and 2021 has role "to"
       3. If the user only specify the start or the end year, we will get the missing start or end year by adding or subtracting 1
    

    entities: list of entity 
    dataManager: DataManager class instance 
    entities: list of entities each entity is a object.
    return: list of sparse matrices represented by pandas dataframe, start year and end year.
    """
    def selectDataToSearchByYear(self, dataManager, intent, entities):
        entityProvidedWithStartAndEndYear = None
        start = None
        end = None
        for entity in entities:
            if entity["entity"] == "year":
                if "role" in entity:
                    if "from" == entity["role"]:
                        start = entity["value"]
                    elif "to" == entity["role"]:
                        end = entity["value"]
                else:
                     entityProvidedWithStartAndEndYear = entity["value"] 

       
        # if no year data is provided, use the most recent data.
        if not  entityProvidedWithStartAndEndYear and not start and not end:
            start, end = dataManager.getMostRecentYearRange()

        if entityProvidedWithStartAndEndYear:
            yearSplitted = entityProvidedWithStartAndEndYear.split("-")
            start = yearSplitted[0]
            end = yearSplitted[1]
        else:
            if start is None and not end is None:

                start = self.calculateYearHelper(end, -1)

            elif not start is None and end is None:
                end = self.calculateYearHelper(start, 1)

        exceptionToThrow = NoDataFoundException(NO_DATA_FOUND_FOR_ACADEMIC_YEAR_ERROR_MESSAGE_FORMAT.format(start=start, end=end), ExceptionTypes.NoDataFoundForAcademicYearException)
        sparseMatrices = dataManager.getSparseMatricesByStartEndYearAndIntent(intent, start, end, exceptionToThrow)
        return (sparseMatrices, start, end)

    def calculateYearHelper(self, year, delta):
        calculatedYear = int(year) + delta
        return str(calculatedYear)
       
        
