# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from Knowledgebase.SparseMatrixKnowledgeBase import SparseMatrixKnowledgeBase

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import sys
import os
# sys.path.append('..')
# print(os.listdir("./"))
from Knowledgebase.ExcelKnowledgeBase import ExcelKnowledgeBase

knowledgeBase = SparseMatrixKnowledgeBase("./Data_Ingestion/CDS_SPARSE_ENR.xlsx")

class ActionGetAvailableOptions(Action):
    def name(self) -> Text:
        return "action_get_available_options"
    
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("For enrollment, you can ask about: how many undergradute students, total graduate students, etc")
        return []


class ActionGetAvailableOptions(Action):
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
        entityValue = []
        for entity in tracker.latest_message['entities']:
            entityValue.append(entity["value"])

        print(tracker.latest_message["intent"])
        print(tracker.latest_message["entities"])
        answer = knowledgeBase.searchForAnswer("_", entityValue)
        dispatcher.utter_message(answer)
        return []
