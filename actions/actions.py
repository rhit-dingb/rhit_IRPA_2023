# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from DataManager.ExcelDataManager import ExcelDataManager
from Knowledgebase.ChooseFromOptionsAddRowStrategy import ChooseFromOptionsAddRowStrategy
from Knowledgebase.DefaultShouldAddRow import DefaultShouldAddRowStrategy
from Knowledgebase.SparseMatrixKnowledgeBase import SparseMatrixKnowledgeBase

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
        answer = knowledgeBase.searchForAnswer(tracker.latest_message["intent"]["name"], entitiesExtracted , selectedShouldAddRowStrategy)
        dispatcher.utter_message(answer)
        return []
