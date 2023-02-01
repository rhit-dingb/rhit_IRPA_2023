# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from CustomEntityExtractor.NumberEntityExtractor import NumberEntityExtractor
from DataManager.ExcelDataManager import ExcelDataManager
from DataManager.constants import ADMISSION_INTENT, BASIS_FOR_SELECTION_INTENT, COHORT_BY_YEAR_ENTITY_LABEL, COHORT_INTENT, ENROLLMENT_INTENT, EXEMPTION_ENTITY_LABEL, FRESHMAN_PROFILE_INTENT, HIGH_SCHOOL_UNITS_INTENT, INITIAL_COHORT_ENTITY_LABEL,  AID_ENTITY_LABEL, NO_AID_ENTITY_LABEL, RANGE_ENTITY_LABEL, RECIPIENT_OF_PELL_GRANT_ENTITY_LABEL, RECIPIENT_OF_STAFFORD_LOAN_NO_PELL_GRANT_ENTITY_LABEL, STUDENT_LIFE_INTENT, TRANSFER_ADMISSION_INTENT, YEAR_FOR_COLLEGE_ENTITY_LABEL
from Exceptions.ExceptionTypes import ExceptionTypes
from Knowledgebase.DefaultShouldAddRow import DefaultShouldAddRowStrategy

from Knowledgebase.IgnoreRowPiece import IgnoreRowPiece
from Knowledgebase.SparseMatrixKnowledgeBase import SparseMatrixKnowledgeBase
from Knowledgebase.constants import PERCENTAGE_FORMAT
from OutputController import output
from actions.constants import AGGREGATION_ENTITY_PERCENTAGE_VALUE, ANY_AID_COLUMN_NAME, NO_AID_COLUMN_NAME, PELL_GRANT_COLUMN_NAME, RANGE_BETWEEN_VALUE, RANGE_UPPER_BOUND_VALUE, STAFFORD_LOAN_COLUMN_NAME, STUDENT_ENROLLMENT_RESULT_ENTITY_GRADUATION_VALUE
from actions.entititesHelper import changeEntityValue, changeEntityValueByRole, copyEntities, createEntityObj, filterEntities, findEntityHelper, findMultipleSameEntitiesHelper
from typing import Text
from DataManager.MongoDataManager import MongoDataManager
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


# ExcelDataManager("./CDSData", [ENROLLMENT_INTENT, COHORT_INTENT, ADMISSION_INTENT, HIGH_SCHOOL_UNITS_INTENT, BASIS_FOR_SELECTION_INTENT, FRESHMAN_PROFILE_INTENT, TRANSFER_ADMISSION_INTENT, STUDENT_LIFE_INTENT])
mongoDataManager = MongoDataManager()
knowledgeBase = SparseMatrixKnowledgeBase(mongoDataManager)



defaultShouldAddRowStrategy = DefaultShouldAddRowStrategy()
numberEntityExtractor = NumberEntityExtractor()

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


class ActionQueryKnowledgebase(Action):
    def name(self) -> Text:
        return "action_query_knowledgebase"

    def run(self, dispatcher, tracker, domain):
        entitiesExtracted = tracker.latest_message["entities"]
        numberEntities = numberEntityExtractor.extractEntities(tracker.latest_message["text"])
        entitiesExtracted = entitiesExtracted + numberEntities
        intent = tracker.latest_message["intent"]["name"]
        print(intent)
        print(entitiesExtracted)
        #try:
        answers = knowledgeBase.searchForAnswer(intent, entitiesExtracted, defaultShouldAddRowStrategy, knowledgeBase.constructOutput,True)
        utterAllAnswers(answers, dispatcher)        
        #except Exception as e:
            #utterAppropriateAnswerWhenExceptionHappen(e, dispatcher)
        return []
    
class ActionSetYear(Action):
    def name(self) -> Text:
        return "action_set_year"
    
    def run(self, dispatcher, tracker, domain):
        pass
        #knowledgeBase.setYear()
    

class ActionQueryCohort(Action):
    def __init__(self) -> None:
        super().__init__()

    def name(self) -> Text:
        return "action_query_cohort"

    def preprocessCohortEntities(self,entities):
        #Since for financial aid part, the entity value may not be extracted perfectly, we map it to the column using entity label
        #Im not sure if this is the best approach but let me know if you have some better idea.
        entityColumnMap = { 
            RECIPIENT_OF_PELL_GRANT_ENTITY_LABEL : PELL_GRANT_COLUMN_NAME,
            RECIPIENT_OF_STAFFORD_LOAN_NO_PELL_GRANT_ENTITY_LABEL: STAFFORD_LOAN_COLUMN_NAME,
            NO_AID_ENTITY_LABEL: NO_AID_COLUMN_NAME
        }

        for key in entityColumnMap.keys():
            changeEntityValueByRole(entities, AID_ENTITY_LABEL, key, entityColumnMap[key])


    def run(self, dispatcher, tracker, domain):
        print(tracker.latest_message["intent"])
        print("ENTITIES")
        # print(tracker.latest_message["entities"])

        entitiesExtracted = tracker.latest_message["entities"]
        intent = tracker.latest_message["intent"]["name"]
        found = list()
        for e in entitiesExtracted:
            # print(e["entity"])
            print(e)
            if "entity" in (e["entity"]):
                found.append(e)

        for e in found:
            entitiesExtracted.remove(e)
        
        print("NEW ENTITIES")
        for e in entitiesExtracted:
            # print(e["entity"])
            print(e)

        self.preprocessCohortEntities(entitiesExtracted)
        #If the user only ask for pell grant or subsized loan of cohort, we should only get the value from the first row, which is the initial cohort
        askPellGrant = findEntityHelper(entitiesExtracted, RECIPIENT_OF_PELL_GRANT_ENTITY_LABEL )
        askStaffordLoan = findEntityHelper(entitiesExtracted, RECIPIENT_OF_STAFFORD_LOAN_NO_PELL_GRANT_ENTITY_LABEL)
        askNoAid = findEntityHelper(entitiesExtracted, NO_AID_ENTITY_LABEL)
    
        filteredEntities = filterEntities(entitiesExtracted, [RECIPIENT_OF_PELL_GRANT_ENTITY_LABEL, RECIPIENT_OF_STAFFORD_LOAN_NO_PELL_GRANT_ENTITY_LABEL, NO_AID_ENTITY_LABEL, COHORT_BY_YEAR_ENTITY_LABEL])
        if (askPellGrant or askStaffordLoan or askNoAid) and len(filteredEntities) == 0:
            entitiesExtracted.append(createEntityObj("initial", INITIAL_COHORT_ENTITY_LABEL))

        # Make a copy of the entities we have so we can still have the original one.
        entitiesExtractedCopy = copyEntities(entitiesExtracted)

        askForPercentage = findEntityHelper(entitiesExtractedCopy, AGGREGATION_ENTITY_PERCENTAGE_VALUE, by="value")
        askForGraduation = findEntityHelper(entitiesExtractedCopy,  STUDENT_ENROLLMENT_RESULT_ENTITY_GRADUATION_VALUE, by = "value")
        askForGraduationRate = askForPercentage and askForGraduation

        ignoreAnyAidShouldAddRow = IgnoreRowPiece(
            defaultShouldAddRowStrategy, [ANY_AID_COLUMN_NAME])
            
        try:
            answers = knowledgeBase.searchForAnswer(intent, entitiesExtracted, ignoreAnyAidShouldAddRow, outputFunc=knowledgeBase.constructOutput)
            utterAllAnswers(answers, dispatcher)
        except Exception as e:
            utterAppropriateAnswerWhenExceptionHappen(e, dispatcher)

        return []

    # def calculateGraduationRate(self,intent, entitiesForNumerator,  filteredEntities , graduatingNumbers, shouldAddRowStrategy):
    #     entitiesToCalculateDenominator = [createEntityObj(FINAL_COHORT_ENTITY_LABEL, entityLabel=FINAL_COHORT_ENTITY_LABEL)]
    #     entitiesToCalculateDenominator = entitiesToCalculateDenominator + filteredEntities
    #     print("ENTITIES TO CALCULATE DENOMINATOR")
    #     print(entitiesToCalculateDenominator)
    #     answer, intent, entities = knowledgeBase.aggregatePercentage(intent, graduatingNumbers, entitiesForNumerator,  entitiesToCalculateDenominator,  shouldAddRowStrategy)
    #     return knowledgeBase.constructOutput(answer, intent, entities)


def utterAllAnswers(answers, dispatcher):
    for answer in answers:
        dispatcher.utter_message(answer)

def utterAppropriateAnswerWhenExceptionHappen(exceptionReceived, dispatcher):
    print(exceptionReceived)
    try:
        exceptionType = exceptionReceived.type
        dispatcher.utter_message(str(exceptionReceived.fallBackMessage))
    except:
        print(exceptionReceived)
        dispatcher.utter_message(
            "Sorry something went wrong, can you please ask again?")
