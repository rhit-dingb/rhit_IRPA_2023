# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


# class ActionHelloWorld(Action):

#     def name(self) -> Text:
#         return "action_hello_world"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hello World!")

#         return []



class ActionGetAvailableOptions(Action):
    def name(self) -> Text:
        return "action_get_available_options"
    
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("For enrollment, you can ask about: how many undergradute students, total graduate students, etc")


class ActionQueryEnrollment(Action):
    def name(self) -> Text:
        return "action_query_enrollment"
    
    def run(self, dispatcher, tracker, domain):
        # we will want to check entities, slot and intents here
        dispatcher.utter_message("Rose-Hulman has 2000 undergraduates")

