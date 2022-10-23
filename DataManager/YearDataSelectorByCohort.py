
from Exceptions.EntityValueException import EntityValueException
from Exceptions.ExceptionMessages import COHORT_YEAR_VALUE_ERROR_MESSAGE_FORMAT, NO_DATA_FOUND_FOR_COHORT_YEAR_ERROR_MESSAGE_FORMAT
from Exceptions.ExceptionTypes import ExceptionTypes
from DataManager.constants import COHORT_BY_YEAR_ENTITY_LABEL, COHORT_INTENT
from Exceptions.NoDataFoundException import NoDataFoundException
from actions.entititesHelper import findEntityHelper

"""
A class used to determine which CDS data to use given the cohort by year.
"""
class YearlyDataSelectorByCohort():

    def selectDataToSearchByYear(self, dataManager, intent : str, entities : object) -> object:
        cohortByYearEntity = findEntityHelper(entities, COHORT_BY_YEAR_ENTITY_LABEL)


        if cohortByYearEntity:
            tokens = cohortByYearEntity["value"].replace("_", " ").split(" ")

            #Handle the case if the intent is cohort (the user ask for cohort info) but they didn't provide the year or if RASA parsed the wrong entity value.
            if len(tokens) == 0:
                raise EntityValueException(COHORT_YEAR_VALUE_ERROR_MESSAGE_FORMAT, 
                ExceptionTypes.CohortByYearEntityValueException)

            year = tokens[0]
            try:
                year = int(year)
            except ValueError as e:
                raise EntityValueException(COHORT_YEAR_VALUE_ERROR_MESSAGE_FORMAT, 
                ExceptionTypes.CohortByYearEntityValueException)

            #Here I am assuming for example 2014 cohort is in 2013-2014 data. However, this may not be the case, we have to ask the client.
            startYear = year -1
            endYear = year

            exceptionToThrow = NoDataFoundException(NO_DATA_FOUND_FOR_COHORT_YEAR_ERROR_MESSAGE_FORMAT.format(year=str(year)), ExceptionTypes.NoDataFoundForCohortYearException)
            sparseMatrices = dataManager.getSparseMatricesByStartEndYearAndIntent(intent, str(startYear), str(endYear), exceptionToThrow); 
            return (sparseMatrices, str(startYear), str(endYear))
        else:
            return (None, -1, -1)

