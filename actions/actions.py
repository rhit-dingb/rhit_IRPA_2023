# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from DataManager.ExcelDataManager import ExcelDataManager
from DataManager.constants import ADMISSION_INTENT, BASIS_FOR_SELECTION_INTENT, COHORT_BY_YEAR_ENTITY_LABEL, COHORT_INTENT, ENROLLMENT_INTENT, EXEMPTION_ENTITY_LABEL, FINAL_COHORT_ENTITY_LABEL, FRESHMAN_PROFILE_INTENT, GRADUATION_RATE_ENTITY_LABEL, HIGH_SCHOOL_UNITS_INTENT, INITIAL_COHORT_ENTITY_LABEL, LOWER_BOUND_GRADUATION_TIME_ENTITY_LABEL, NO_AID_ENTITY_LABEL, RECIPIENT_OF_PELL_GRANT_ENTITY_LABEL, RECIPIENT_OF_STAFFORD_LOAN_NO_PELL_GRANT_ENTITY_LABEL, RETENTION_RATE_LABEL, TRANSFER_ADMISSION_INTENT, UPPER_BOUND_GRADUATION_TIME_ENTITY_LABEL
from Exceptions.ExceptionTypes import ExceptionTypes
from Knowledgebase.DefaultShouldAddRow import DefaultShouldAddRowStrategy

from Knowledgebase.IgnoreRowPiece import IgnoreRowPiece
from Knowledgebase.SparseMatrixKnowledgeBase import SparseMatrixKnowledgeBase
from Knowledgebase.constants import PERCENTAGE_FORMAT
from OutputController import output
from actions.constants import ANY_AID_COLUMN_NAME, COHORT_GRADUATION_TIME_ENTITY_FORMAT, COHORT_GRADUATION_TIME_START_FORMAT, NO_AID_COLUMN_NAME, PELL_GRANT_COLUMN_NAME, STAFFORD_LOAN_COLUMN_NAME
from actions.entititesHelper import changeEntityValue, copyEntities, createEntityObj, filterEntities, findEntityHelper, findMultipleSameEntitiesHelper
from typing import List, Text, Tuple

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# knowledgeBase = SparseMatrixKnowledgeBase("./Data_Ingestion/CDS_SPARSE_ENR.xlsx")


knowledgeBase = SparseMatrixKnowledgeBase(ExcelDataManager("./CDSData", [ENROLLMENT_INTENT, COHORT_INTENT, ADMISSION_INTENT, HIGH_SCHOOL_UNITS_INTENT, BASIS_FOR_SELECTION_INTENT, FRESHMAN_PROFILE_INTENT, TRANSFER_ADMISSION_INTENT]))

# This is a dictionary storing for an intent, what entities must be detected in the user's question in order for a answer to be returned
# For example in the freshman profile, percentage is a column in the sparse matrix and an entity. If the user provide some bad input like:
# "what is the percentage?", it would add up all the percentage row and return an answer that makes no sense.
requiredEntitiesMap = {
    FRESHMAN_PROFILE_INTENT: [
        "act", 'sat'
    ]
}


defaultShouldAddRowStrategy = DefaultShouldAddRowStrategy()

class ActionGetAvailableOptions(Action):
    def name(self) -> Text:
        return "action_get_available_options"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(
            "For enrollment, you can ask about: how many undergradute students, total graduate students, etc")
        return []


class ActionAskMoreQuestion(Action):
    def name(self) -> Text:
        return "action_ask_more_question"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("Great! Do you have anymore questions?")
        return []

class ActionQueryTransferAdmission(Action):
   
    def name(self) -> Text:
        return  "action_query_transfer_admission"

    def run(self, dispatcher, tracker, domain):
        entitiesExtracted = tracker.latest_message["entities"]
        intent = tracker.latest_message["intent"]["name"]
        print(entitiesExtracted)
        try:
            answers = knowledgeBase.searchForAnswer(intent, entitiesExtracted, defaultShouldAddRowStrategy, knowledgeBase.constructOutput, True)
            utterAllAnswers(answers, dispatcher)   
            
        except Exception as e:
            utterAppropriateAnswerWhenExceptionHappen(e, dispatcher)
            

        return []


class ActionQueryFreshmanProfile(Action):
    def __init__(self) -> None:
        super().__init__()
        
    def name(self) -> Text:
        return "action_query_freshman_profile"
    
    def run(self, dispatcher, tracker, domain):
        entitiesExtracted = tracker.latest_message["entities"]
        intent = tracker.latest_message["intent"]["name"]
        print(entitiesExtracted)

        # I will not check for required entity for now.
        # requiredEntityPresent = checkIfRequiredEntityIsPresent(intent, entitiesExtracted)
        # NO_REQUIRED_ENTITY_PRESENT_MESSAGE = "Sorry I do not understand, please rephrase your question by being more specific"
        # if not requiredEntityPresent: 
        #     dispatcher.utter_message(NO_REQUIRED_ENTITY_PRESENT_MESSAGE)
        #     return []

        try:
            answers = knowledgeBase.searchForAnswer(intent, entitiesExtracted, defaultShouldAddRowStrategy, knowledgeBase.constructOutput, True)
            utterAllAnswers(answers, dispatcher)   
            
        except Exception as e:
            utterAppropriateAnswerWhenExceptionHappen(e, dispatcher)
            
        return []
        
class ActionQueryBasisForSelection(Action):
    def __init__(self) -> None:
        super().__init__()
        
    def name(self) -> Text:
        return "action_query_basis_for_selection"
    
    def run(self, dispatcher, tracker, domain):
        entitiesExtracted = tracker.latest_message["entities"]
        intent = tracker.latest_message["intent"]["name"]
        
        print(entitiesExtracted)
        try:
            answers = knowledgeBase.searchForAnswer(intent, entitiesExtracted, defaultShouldAddRowStrategy, knowledgeBase.constructOutput)
            utterAllAnswers(answers, dispatcher)   
            
        except Exception as e:
            utterAppropriateAnswerWhenExceptionHappen(e, dispatcher)
        
        return []



class ActionQueryHighSchoolUnits(Action):
    def __init__(self) -> None:
        super().__init__()
 
        self.choosenShouldAddRowStrategy = DefaultShouldAddRowStrategy()
        
    def name(self) -> Text:
        return "action_query_high_school_units"

    def run(self, dispatcher, tracker, domain):
        entitiesExtracted = tracker.latest_message["entities"]
        intent = tracker.latest_message["intent"]["name"]
        print(tracker.latest_message["intent"])
        print(tracker.latest_message["entities"])
        
        try:
            answers = knowledgeBase.searchForAnswer(intent, entitiesExtracted, self.choosenShouldAddRowStrategy, output.outputFuncForHighSchoolUnits)
            utterAllAnswers(answers, dispatcher)  
        except Exception as e:
           utterAppropriateAnswerWhenExceptionHappen(e, dispatcher)


class ActionQueryEnrollment(Action):
    def __init__(self) -> None:
        pass


    def name(self) -> Text:
        return "action_query_enrollment"

    def run(self, dispatcher, tracker, domain):

        haveRaceEnrollmentEntity = False
        entitiesExtracted = tracker.latest_message["entities"]
        print(entitiesExtracted)

        intent = tracker.latest_message["intent"]["name"]
        print(intent)

        for entityObj in tracker.latest_message['entities']:
            if entityObj["entity"] == "race":
                haveRaceEnrollmentEntity = True
                
        selectedShouldAddRowStrategy = defaultShouldAddRowStrategy
        if haveRaceEnrollmentEntity:
            selectedShouldAddRowStrategy = defaultShouldAddRowStrategy

        try:
            answers = knowledgeBase.searchForAnswer(
                        tracker.latest_message["intent"]["name"], entitiesExtracted, selectedShouldAddRowStrategy, knowledgeBase.constructOutput)
            utterAllAnswers(answers, dispatcher)
        except Exception as e:
            utterAppropriateAnswerWhenExceptionHappen(e, dispatcher)

        return []


class ActionQueryAdmission(Action):
    def name(self) -> Text:
        return "action_query_admission"

    def run(self, dispatcher, tracker, domain):

      
        entitiesExtracted = tracker.latest_message["entities"]
        selectedShouldAddRowStrategy = defaultShouldAddRowStrategy

        print(entitiesExtracted)
        try:
            answers = knowledgeBase.searchForAnswer(
                tracker.latest_message["intent"]["name"], entitiesExtracted, selectedShouldAddRowStrategy,knowledgeBase.constructOutput)
            utterAllAnswers(answers, dispatcher)
        except Exception as e:
            utterAppropriateAnswerWhenExceptionHappen(e, dispatcher)

        return []

class ActionQueryCohort(Action):
    def __init__(self) -> None:
        super().__init__()
        self.maxYear = 6
        self.minYear = 4
        self.currentOutputFunc =  output.outputFuncForInteger

    def name(self) -> Text:
        return "action_query_cohort"

    def extractYearFromGraduationYearEntityValue(self, entitiesFound):
        
        if entitiesFound is None or len(entitiesFound) == 0:
            return -1

        indexes = []

        for entityObj in entitiesFound:
            for i in range(self.minYear, self.maxYear+1):
                index_value = None
                try:
                    index_value = entityObj["value"].index(str(i))
                    
                except ValueError:
                    index_value = -1

                indexes.append(index_value)

            for index in indexes:
                if index > -1:
                    return int(entityObj["value"][index])

        return -1

    def preprocessCohortEntities(self,entities):
        #Since for financial aid part, the entity value may not be extracted perfectly, we map it to the column using entity label
        #Im not sure if this is the best approach but let me know if you have some better idea.
        entityColumnMap = { 
            RECIPIENT_OF_PELL_GRANT_ENTITY_LABEL : PELL_GRANT_COLUMN_NAME,
            RECIPIENT_OF_STAFFORD_LOAN_NO_PELL_GRANT_ENTITY_LABEL: STAFFORD_LOAN_COLUMN_NAME,
            NO_AID_ENTITY_LABEL: NO_AID_COLUMN_NAME
        }

        for key in entityColumnMap.keys():
            changeEntityValue(entities, key, entityColumnMap[key])



    def run(self, dispatcher, tracker, domain):
        print(tracker.latest_message["intent"])
        print("ENTITIES")
        print(tracker.latest_message["entities"])

        entitiesExtracted = tracker.latest_message["entities"]
        intent = tracker.latest_message["intent"]["name"]

        self.preprocessCohortEntities(entitiesExtracted)
        
        
        #If the user only ask for pell grant or subsized loan of cohort, we should only get the value from the first row, which is the initial cohort
        askPellGrant = findEntityHelper(entitiesExtracted, RECIPIENT_OF_PELL_GRANT_ENTITY_LABEL )
        askStaffordLoan = findEntityHelper(entitiesExtracted, RECIPIENT_OF_STAFFORD_LOAN_NO_PELL_GRANT_ENTITY_LABEL)
        askNoAid = findEntityHelper(entitiesExtracted, NO_AID_ENTITY_LABEL)
        
        askRetentionRate = findEntityHelper(entitiesExtracted, RETENTION_RATE_LABEL )
    
        filteredEntities = filterEntities(entitiesExtracted, [RECIPIENT_OF_PELL_GRANT_ENTITY_LABEL, RECIPIENT_OF_STAFFORD_LOAN_NO_PELL_GRANT_ENTITY_LABEL, NO_AID_ENTITY_LABEL, COHORT_BY_YEAR_ENTITY_LABEL])
        if (askPellGrant or askStaffordLoan or askNoAid) and len(filteredEntities) == 0:
            entitiesExtracted.append(createEntityObj("initial", INITIAL_COHORT_ENTITY_LABEL))
        
        
        # we might want to refactor this later with some classes.
        def generator(curr, start, end):
            if curr == self.minYear:
                return COHORT_GRADUATION_TIME_START_FORMAT.format(upperBound=self.minYear)
            else:
                return COHORT_GRADUATION_TIME_ENTITY_FORMAT.format(upperBound=curr, lowerBound=curr-1)

        entitiesExtractedCopy = copyEntities(entitiesExtracted)

        askForGraduationRate = findEntityHelper(
            entitiesExtractedCopy, GRADUATION_RATE_ENTITY_LABEL)

        lowerBoundGraduationYearEntities = findMultipleSameEntitiesHelper(
            entitiesExtractedCopy, LOWER_BOUND_GRADUATION_TIME_ENTITY_LABEL)
        upperBoundGraduationYearEntities = findMultipleSameEntitiesHelper(
            entitiesExtractedCopy, UPPER_BOUND_GRADUATION_TIME_ENTITY_LABEL)

        ignoreAnyAidShouldAddRow = IgnoreRowPiece(
            defaultShouldAddRowStrategy, [ANY_AID_COLUMN_NAME])
            
        if (askForGraduationRate and len(entitiesExtracted) == 2) or lowerBoundGraduationYearEntities or upperBoundGraduationYearEntities:
            # For question about graduation date and year,the initial and final entity is still extracted, but I want to filter that out.
            entitiesFiltered = filterEntities(entitiesExtractedCopy, [
                                                LOWER_BOUND_GRADUATION_TIME_ENTITY_LABEL, UPPER_BOUND_GRADUATION_TIME_ENTITY_LABEL, INITIAL_COHORT_ENTITY_LABEL, FINAL_COHORT_ENTITY_LABEL])
            lowerBoundYear = max(self.extractYearFromGraduationYearEntityValue(
                lowerBoundGraduationYearEntities)+1, self.minYear)
      

        
            upperBoundYear = min(self.extractYearFromGraduationYearEntityValue(
                upperBoundGraduationYearEntities), self.maxYear)

            # print("UPPER BOUND YEAR")
            # print(upperBoundYear)

            isUpperFoundBoundNotFound = upperBoundYear == -1
            if isUpperFoundBoundNotFound:
                upperBoundYear = self.maxYear
            
            # print(lowerBoundYear, upperBoundYear)
            
            answer = None

            try:
                answer, intent, entitiesUsed = knowledgeBase.aggregateDiscreteRange(
                intent, entitiesFiltered, lowerBoundYear, upperBoundYear, generator, ignoreAnyAidShouldAddRow,
                )

                if askForGraduationRate:
                    entitiesUsed.add(askForGraduationRate["value"])
                    answer = self.calculateGraduationRate(intent, entitiesUsed, entitiesFiltered, float(answer), ignoreAnyAidShouldAddRow)
                
                else:
                    answer = output.outputFuncForInteger(answer, intent, entitiesUsed)
                
                dispatcher.utter_message(answer)    
            except Exception as e:
                 utterAppropriateAnswerWhenExceptionHappen(e, dispatcher)        
            
        else:
            
            try:
                answers = knowledgeBase.searchForAnswer(intent, entitiesExtracted, ignoreAnyAidShouldAddRow, outputFunc=knowledgeBase.constructOutput)
                utterAllAnswers(answers, dispatcher)
            except Exception as e:
                utterAppropriateAnswerWhenExceptionHappen(e, dispatcher)

        return []

    def calculateGraduationRate(self,intent, entitiesForNumerator,  filteredEntities , graduatingNumbers, shouldAddRowStrategy):
        entitiesToCalculateDenominator = [createEntityObj(FINAL_COHORT_ENTITY_LABEL, entityLabel=FINAL_COHORT_ENTITY_LABEL)]
        entitiesToCalculateDenominator = entitiesToCalculateDenominator + filteredEntities
        print("ENTITIES TO CALCULATE DENOMINATOR")
        print(entitiesToCalculateDenominator)
        answer, intent, entities = knowledgeBase.aggregatePercentage(intent, graduatingNumbers, entitiesForNumerator,  entitiesToCalculateDenominator,  shouldAddRowStrategy)
        return knowledgeBase.constructOutput(answer, intent, entities)


def utterAllAnswers(answers, dispatcher):
    for answer in answers:
        dispatcher.utter_message(answer)

def checkIfRequiredEntityIsPresent(intent, entities):
    if not intent in requiredEntitiesMap:
        return True
    else:
        requiredEntities = requiredEntitiesMap[intent]
        for entity in entities:
            if entity["value"] in requiredEntities:
                return True 
    return False

def utterAppropriateAnswerWhenExceptionHappen(exceptionReceived, dispatcher):
    print(exceptionReceived)
    try:
        exceptionType = exceptionReceived.type
        dispatcher.utter_message(str(exceptionReceived.fallBackMessage))
    except:
        print(exceptionReceived)
        dispatcher.utter_message(
            "Sorry something went wrong, can you please ask again?")
