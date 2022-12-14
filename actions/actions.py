# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from DataManager.ExcelDataManager import ExcelDataManager
from DataManager.constants import ADMISSION_INTENT, BASIS_FOR_SELECTION_INTENT, COHORT_BY_YEAR_ENTITY_LABEL, COHORT_INTENT, ENROLLMENT_INTENT, EXEMPTION_ENTITY_LABEL, FINAL_COHORT_ENTITY_LABEL, FRESHMAN_PROFILE_INTENT, HIGH_SCHOOL_UNITS_INTENT, INITIAL_COHORT_ENTITY_LABEL,  AID_ENTITY_LABEL, NO_AID_ENTITY_LABEL, RANGE_ENTITY_LABEL, RECIPIENT_OF_PELL_GRANT_ENTITY_LABEL, RECIPIENT_OF_STAFFORD_LOAN_NO_PELL_GRANT_ENTITY_LABEL, STUDENT_LIFE_INTENT, TRANSFER_ADMISSION_INTENT, YEAR_FOR_COLLEGE_ENTITY_LABEL
from Exceptions.ExceptionTypes import ExceptionTypes
from Knowledgebase.DefaultShouldAddRow import DefaultShouldAddRowStrategy

from Knowledgebase.IgnoreRowPiece import IgnoreRowPiece
from Knowledgebase.SparseMatrixKnowledgeBase import SparseMatrixKnowledgeBase
from Knowledgebase.constants import PERCENTAGE_FORMAT
from OutputController import output
from actions.constants import AGGREGATION_ENTITY_PERCENTAGE_VALUE, ANY_AID_COLUMN_NAME, NO_AID_COLUMN_NAME, PELL_GRANT_COLUMN_NAME, RANGE_BETWEEN_VALUE, RANGE_LOWER_BOUND_VALUE, RANGE_UPPER_BOUND_VALUE, STAFFORD_LOAN_COLUMN_NAME, STUDENT_ENROLLMENT_RESULT_ENTITY_GRADUATION_VALUE, STUDENT_ENROLLMENT_RESULT_ENTITY_RETENTION_VALUE, YEARS_FOR_COLLEGE_ENTITY_FORMAT
from actions.entititesHelper import changeEntityValue, changeEntityValueByRole, copyEntities, createEntityObj, filterEntities, findEntityHelper, findMultipleSameEntitiesHelper
from typing import Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# knowledgeBase = SparseMatrixKnowledgeBase("./Data_Ingestion/CDS_SPARSE_ENR.xlsx")


knowledgeBase = SparseMatrixKnowledgeBase(ExcelDataManager("./CDSData", [ENROLLMENT_INTENT, COHORT_INTENT, ADMISSION_INTENT, HIGH_SCHOOL_UNITS_INTENT, BASIS_FOR_SELECTION_INTENT, FRESHMAN_PROFILE_INTENT, TRANSFER_ADMISSION_INTENT
, STUDENT_LIFE_INTENT]))

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


class ActionQueryKnowledgebase(Action):
    def name(self) -> Text:
        return "action_query_knowledgebase"

    def run(self, dispatcher, tracker, domain):
        entitiesExtracted = tracker.latest_message["entities"]
        intent = tracker.latest_message["intent"]["name"]
        print(intent)
        print(entitiesExtracted)
        try:
            answers = knowledgeBase.searchForAnswer(intent, entitiesExtracted, defaultShouldAddRowStrategy, knowledgeBase.constructOutput, True)
            utterAllAnswers(answers, dispatcher)        
        except Exception as e:
            utterAppropriateAnswerWhenExceptionHappen(e, dispatcher)
        return []
    


class ActionQueryTransferAdmission(Action):
   
    def name(self) -> Text:
        return  "action_query_transfer_admission"

    def run(self, dispatcher, tracker, domain):
        entitiesExtracted = tracker.latest_message["entities"]
        intent = tracker.latest_message["intent"]["name"]
        print(intent)
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
        print(intent)
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
        print(intent)
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
            answers = knowledgeBase.searchForAnswer(intent, entitiesExtracted, self.choosenShouldAddRowStrategy, knowledgeBase.constructOutput)
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
<<<<<<< HEAD
        print(tracker.latest_message["intent"]["name"])
        print(entitiesExtracted)
=======
        print(entitiesExtracted)

        intent = tracker.latest_message["intent"]["name"]
        print(intent)

>>>>>>> winter_iteration_3
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
        print(tracker.latest_message["intent"]["name"])
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


    def findYearRange(self, entitiesFound):
        minYear = self.minYear
        maxYear = self.maxYear
        yearsFound = [] 
        for entityObj in entitiesFound:
            for i in range(self.minYear, self.maxYear+1):
                index_value = None
                try:
                    index_value = entityObj["value"].index(str(i))
                    year = int(entityObj["value"][index_value])
                    print("YEAR")
                    print(year)
                    print(entityObj["value"])
                    yearsFound.append(year)
                except ValueError:
                    continue

        askForUpperBound = findEntityHelper(entitiesFound, RANGE_UPPER_BOUND_VALUE, by = "value")
        askForLowerBound = findEntityHelper(entitiesFound, RANGE_LOWER_BOUND_VALUE, by = "value")

        if len(yearsFound) > 1:

            maxYear = max(yearsFound)
            minYear = min(yearsFound)

            # I add one here, because when the user ask "more than"(lower bound) it means they want more than that year instead of including that year
            if askForLowerBound:
                minYear = minYear+1
        
        elif len(yearsFound) == 1:
            

            if askForUpperBound:
                minYear = self.minYear
                maxYear = max(yearsFound)
            elif askForLowerBound:
                maxYear = self.maxYear
                minYear = min(yearsFound)+1
            #Handle the case when no upper bound or lower bound is specified, default to upperbound
            else: 
                minYear = self.minYear
                maxYear = max(yearsFound)

        #Making sure the max year and minYear stays in valid range
        maxYear = min(maxYear, self.maxYear)
        minYear = max(minYear,self.minYear)
        return (minYear, maxYear)


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
        print(intent)
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

        print("PROCESSED ENTITIES")
        for e in entitiesExtracted:
            # print(e["entity"])
            print(e)
        
        
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
        askForRetention = findEntityHelper(entitiesExtractedCopy, STUDENT_ENROLLMENT_RESULT_ENTITY_RETENTION_VALUE, by = "value")
        askForGraduationRate = askForPercentage and askForGraduation
        askRetentionRate = askForPercentage and askForRetention

        yearForCollegeEntity = findEntityHelper(entitiesExtractedCopy, YEAR_FOR_COLLEGE_ENTITY_LABEL )

        ignoreAnyAidShouldAddRow = IgnoreRowPiece(
            defaultShouldAddRowStrategy, [ANY_AID_COLUMN_NAME])
            

        if askForGraduationRate  or yearForCollegeEntity:
            # For question about graduation date and year,the initial and final entity is still extracted, but I want to filter that out.
            entitiesFiltered = filterEntities(entitiesExtractedCopy, [INITIAL_COHORT_ENTITY_LABEL, FINAL_COHORT_ENTITY_LABEL])
            yearsOfCollegeEntities = findMultipleSameEntitiesHelper(entitiesExtractedCopy, YEAR_FOR_COLLEGE_ENTITY_LABEL)
            rangeEntities = findMultipleSameEntitiesHelper(entitiesExtractedCopy, RANGE_ENTITY_LABEL)

            yearsOfCollegeAndRangeEntities = yearsOfCollegeEntities + rangeEntities
            minYear, maxYear = self.findYearRange(yearsOfCollegeAndRangeEntities)
            print(minYear, maxYear)
            entitiesFiltered = filterEntities(entitiesFiltered, [YEAR_FOR_COLLEGE_ENTITY_LABEL, RANGE_ENTITY_LABEL])
            
            answer = None

            def generator(curr, start, end):
                if curr == self.minYear:
                    return [RANGE_UPPER_BOUND_VALUE, YEARS_FOR_COLLEGE_ENTITY_FORMAT.format(year=curr) ]
                else:
                    print(RANGE_BETWEEN_VALUE, YEARS_FOR_COLLEGE_ENTITY_FORMAT.format(year = curr))
                    return [RANGE_BETWEEN_VALUE, YEARS_FOR_COLLEGE_ENTITY_FORMAT.format(year = curr), YEARS_FOR_COLLEGE_ENTITY_FORMAT.format(year = curr-1)]

            try:    
                answer, intent, entitiesUsed = knowledgeBase.aggregateDiscreteRange(
                    intent, entitiesFiltered, minYear, maxYear, generator, ignoreAnyAidShouldAddRow
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
