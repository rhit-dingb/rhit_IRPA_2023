# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from copy import deepcopy
from re import L
from DataManager.ExcelDataManager import ExcelDataManager
from DataManager.constants import INITIAL_COHORT_ENTITY_LABEL, LOWER_BOUND_GRADUATION_TIME_ENTITY_LABEL, UPPER_BOUND_GRADUATION_TIME_ENTITY_LABEL
from Exceptions.ExceptionTypes import ExceptionTypes
from Knowledgebase.ChooseFromOptionsAddRowStrategy import ChooseFromOptionsAddRowStrategy
from Knowledgebase.DefaultShouldAddRow import DefaultShouldAddRowStrategy
from Knowledgebase.IgnoreRowPiece import IgnoreRowPiece
from Knowledgebase.SparseMatrixKnowledgeBase import SparseMatrixKnowledgeBase
from actions.constants import ANY_AID_COLUMN_NAME, COHORT_GRADUATION_TIME_ENTITY_FORMAT, COHORT_GRADUATION_TIME_START_FORMAT
from actions.entititesHelper import copyEntities, filterEntities, findEntityHelper
from typing import Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# knowledgeBase = SparseMatrixKnowledgeBase("./Data_Ingestion/CDS_SPARSE_ENR.xlsx")

knowledgeBase = SparseMatrixKnowledgeBase(ExcelDataManager("./CDSData"))

defaultShouldAddRowStrategy = DefaultShouldAddRowStrategy()
chooseFromOptionsAddRowStrategy = ChooseFromOptionsAddRowStrategy(choices=[{
            "columns": ["degree-seeking", "first-time", "first-year"]
        }, 
        {
            "columns": ["degree-seeking", "non-first-time", "non-first-year"],
            "isDefault":True
        }])


class ActionGetAvailableOptions(Action):
    def name(self) -> Text:
        return "action_get_available_options"
    
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("For enrollment, you can ask about: how many undergradute students, total graduate students, etc")
        return []


class ActionAskMoreQuestion(Action):
    def name(self) -> Text:
        return "action_ask_more_question"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("Great! Do you have anymore questions?")
        return []

class ActionQueryEnrollment(Action):
    def name(self) -> Text:
        return "action_query_enrollment"
    
    def run(self, dispatcher, tracker, domain):
        # we will want to check entities, slot and intents here
        # refactor this once the knowledge base is changed into sparse matrix form
        haveRaceEnrollmentEntity = False
        entitiesExtracted = tracker.latest_message["entities"]
        for entityObj in tracker.latest_message['entities']:
            if entityObj["entity"] == "race":
                haveRaceEnrollmentEntity = True
           
        
        print(tracker.latest_message["intent"])
        print(tracker.latest_message["entities"])
        selectedShouldAddRowStrategy = defaultShouldAddRowStrategy
        if haveRaceEnrollmentEntity:
            selectedShouldAddRowStrategy = chooseFromOptionsAddRowStrategy

        answer = None
        try:
            answer = knowledgeBase.searchForAnswer(tracker.latest_message["intent"]["name"], entitiesExtracted , selectedShouldAddRowStrategy)
            dispatcher.utter_message(answer)
        except Exception as e:
            utterAppropriateAnswerWhenExceptionHappen(e, dispatcher)
      
        
        return []

class ActionQueryCohort(Action):

    def name(self) -> Text:
        return "action_query_cohort"
    
    def extractYearFromGraduationYearEntityValue(self, entityObj ):

        if entityObj is None:
            return -1 

        indexes = []
    
        for i in range(4,6+1):
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

   
    def run(self, dispatcher, tracker, domain):
        print(tracker.latest_message["intent"])
        print(tracker.latest_message["entities"])

        entitiesExtracted = tracker.latest_message["entities"]
        intent = tracker.latest_message["intent"]["name"]

        # we might want to refactor this later with some classes.
             
        maxYear = 6
        minYear = 4

        def generator(curr, start, end):
            if curr == minYear:
                return COHORT_GRADUATION_TIME_START_FORMAT.format(upperBound = minYear )
            else:
                return COHORT_GRADUATION_TIME_ENTITY_FORMAT.format(upperBound =curr, lowerBound = curr-1)
        
        entitiesExtractedCopy = copyEntities(entitiesExtracted)
        askForGraduationRate = findEntityHelper(entitiesExtractedCopy, "graduation_rate")
        lowerBoundGraduationYearEntity = findEntityHelper(entitiesExtractedCopy, LOWER_BOUND_GRADUATION_TIME_ENTITY_LABEL)
        upperBoundGraduationYearEntity = findEntityHelper(entitiesExtractedCopy, UPPER_BOUND_GRADUATION_TIME_ENTITY_LABEL)
    
        if lowerBoundGraduationYearEntity or upperBoundGraduationYearEntity:
            #For question about graduation date and year,the initial entity is still extracted, but I want to filter that out.
            entitiesFiltered = filterEntities(entitiesExtractedCopy, [lowerBoundGraduationYearEntity["entity"],upperBoundGraduationYearEntity["entity"]
            , INITIAL_COHORT_ENTITY_LABEL ])
           
            lowerBoundYear = max(self.extractYearFromGraduationYearEntityValue(lowerBoundGraduationYearEntity)+1, minYear)
            upperBoundYear = min(self.extractYearFromGraduationYearEntityValue(upperBoundGraduationYearEntity), maxYear)

            answer = None

            ignoreAnyAidShouldAddRow = IgnoreRowPiece(defaultShouldAddRowStrategy, [ANY_AID_COLUMN_NAME])

            try:
                answer = knowledgeBase.aggregateDiscreteRange(intent, entitiesFiltered, lowerBoundYear, upperBoundYear, generator, ignoreAnyAidShouldAddRow)
                dispatcher.utter_message(answer)
            except Exception as e:
               utterAppropriateAnswerWhenExceptionHappen(e, dispatcher)
        else:
            knowledgeBase.searchForAnswer(intent, entitiesExtracted, defaultShouldAddRowStrategy)   

        return []


def utterAppropriateAnswerWhenExceptionHappen(exceptionReceived, dispatcher):
    if exceptionReceived.type:
        dispatcher.utter_message(str(exceptionReceived.fallBackMessage))
    else:
        dispatcher.utter_message("Sorry something went wrong, can you please ask again?")