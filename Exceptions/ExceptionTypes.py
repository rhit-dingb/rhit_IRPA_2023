from enum import Enum

from Exceptions.ExceptionMessages import COHORT_YEAR_VALUE_ERROR_MESSAGE_FORMAT
from enum import Enum, auto
class ExceptionTypes(Enum):
    CohortByYearEntityValueException = auto()
    NoDataFoundForAcademicYearException = auto()
    NoDataFoundForCohortYearException = auto() 
    NotEnoughDataForCohortYearException = auto()
