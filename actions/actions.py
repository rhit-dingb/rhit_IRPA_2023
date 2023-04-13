# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


import asyncio
import json
import requests
from CacheLayer.Cache import Cache
from enum import Enum


from CustomEntityExtractor.NumberEntityExtractor import NumberEntityExtractor
from DataManager.ExcelDataManager import ExcelDataManager
from DataManager.constants import  COHORT_BY_YEAR_ENTITY_LABEL, COHORT_INTENT, ENROLLMENT_INTENT, EXEMPTION_ENTITY_LABEL, FRESHMAN_PROFILE_INTENT, HIGH_SCHOOL_UNITS_INTENT, INITIAL_COHORT_ENTITY_LABEL,  AID_ENTITY_LABEL, NO_AID_ENTITY_LABEL, RANGE_ENTITY_LABEL, RECIPIENT_OF_PELL_GRANT_ENTITY_LABEL, RECIPIENT_OF_STAFFORD_LOAN_NO_PELL_GRANT_ENTITY_LABEL, STUDENT_LIFE_INTENT, TRANSFER_ADMISSION_INTENT, YEAR_FOR_COLLEGE_ENTITY_LABEL
from Exceptions.ExceptionTypes import ExceptionTypes
from Knowledgebase.DefaultShouldAddRow import DefaultShouldAddRowStrategy

from Knowledgebase.IgnoreRowPiece import IgnoreRowPiece
from Knowledgebase.SparseMatrixKnowledgeBase import SparseMatrixKnowledgeBase
from OutputController import output

from actions.constants import  BACKEND_API_URL, LAST_ANSWERS_PROVIDED_SLOT_NAME, YEAR_RANGE_SELECTED_SLOT_NAME, AGGREGATION_ENTITY_PERCENTAGE_VALUE, ANY_AID_COLUMN_NAME, NO_AID_COLUMN_NAME, PELL_GRANT_COLUMN_NAME, RANGE_BETWEEN_VALUE, RANGE_UPPER_BOUND_VALUE, STAFFORD_LOAN_COLUMN_NAME, STUDENT_ENROLLMENT_RESULT_ENTITY_GRADUATION_VALUE
from actions.entititesHelper import changeEntityValue, changeEntityValueByRole, copyEntities, createEntityObj, filterEntities, findEntityHelper, findMultipleSameEntitiesHelper, getEntityLabel, getEntityValueHelper, removeDuplicatedEntities
from typing import Dict, List, Text
from DataManager.MongoDataManager import MongoDataManager
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from actions.ResponseType import ResponseType
from actions.constants import LAST_TOPIC_INTENT_SLOT_NAME, LAST_USER_QUESTION_ASKED

from Data_Ingestion.ConvertToSparseMatrixDecorator import ConvertToSparseMatrixDecorator
from Data_Ingestion.MongoProcessor import MongoProcessor
# from Knowledgebase.QuestionAnswerKnowledgebase.QuestionAnswerKnowledgebase import QuestionAnswerKnowledgeBase
from Data_Ingestion.ConvertToDocumentDecorator import ConvertToDocumentDecorator

# import backendAPI.general_api  as API 
import nltk

from Knowledgebase.Knowledgebase import KnowledgeBase
from Knowledgebase.QuestionAnswerKnowledgebase.QuestionAnswerKnowledgebase import QuestionAnswerKnowledgeBase
from Knowledgebase.QuestionAnswerKnowledgebase.FAQKnowledgebase import FAQKnowledgeBase
from Knowledgebase.DataModels.ChatbotAnswer import ChatbotAnswer
from Knowledgebase.DataModels.FeedbackLabel import FeedbackLabel, FeedbackType
from Knowledgebase.DataModels.MultiFeedbackLabel import MultiFeedbackLabel




try:
    nltk.find('corpora/wordnet')
except Exception:
    nltk.download('wordnet')

try:
    nltk.find('omw-1.4')
except Exception:
    nltk.download('omw-1.4')

# ExcelDataManager("./CDSData", [ENROLLMENT_INTENT, COHORT_INTENT, ADMISSION_INTENT, HIGH_SCHOOL_UNITS_INTENT, BASIS_FOR_SELECTION_INTENT, FRESHMAN_PROFILE_INTENT, TRANSFER_ADMISSION_INTENT, STUDENT_LIFE_INTENT])

numberEntityExtractor = NumberEntityExtractor()

mongoProcessor = MongoProcessor()
mongoProcessor = ConvertToSparseMatrixDecorator(mongoProcessor)
mongoDataManager = MongoDataManager(mongoProcessor)

mongoDataManager = Cache(mongoDataManager)
sparseMatrixKnowledgeBase = SparseMatrixKnowledgeBase(mongoDataManager)


mongoProcessor = MongoProcessor()
mongoProcessor = ConvertToDocumentDecorator(mongoProcessor)
mongoDataManager = MongoDataManager(mongoProcessor)
qaKnowledgebase = QuestionAnswerKnowledgeBase(mongoDataManager)
asyncio.run(qaKnowledgebase.initialize())


# mongoProcessor = MongoProcessor()
# mongoProcessor = ConvertToDocumentDecorator(mongoProcessor)
# mongoDataManager = MongoDataManager(mongoProcessor)
# faqKnowledgebase = FAQKnowledgeBase(mongoDataManager)
# asyncio.run(faqKnowledgebase.initialize())



knowledgebaseEnsemble : List[KnowledgeBase] = [sparseMatrixKnowledgeBase, qaKnowledgebase]

class ActionGetAvailableOptions(Action):
    def __init__(self) -> None:
        super().__init__()
        self.HEADER_MESSAGE_TEMPLATE = "Here is a available list of topics you can ask me about for the {start_year}-{end_year} academic year"

    def name(self) -> Text:
        return "action_get_available_options"

    def run(self, dispatcher, tracker, domain):
        lastTopicIntent = tracker.get_slot(LAST_TOPIC_INTENT_SLOT_NAME)
      
        # print("LAST INTENT")
        # print(lastTopicIntent)
        startYear, endYear, res = getYearRangeInSlot(tracker)
        allIntents = list(map(lambda x: x.replace("_", " "), domain["intents"]))
        filteredListOfOption = dict()
        availableOptions = mongoDataManager.getAvailableOptions(None, startYear, endYear)
      
        for option in availableOptions:
            if option in allIntents:
                filteredListOfOption[option] = availableOptions[option]
    
        headerMessage = self.HEADER_MESSAGE_TEMPLATE.format(start_year = startYear, end_year = endYear)
        response = {"type": ResponseType.ACCORDION_LIST.value, "header": headerMessage, "data": filteredListOfOption}
     
        dispatcher.utter_message(json_message= response)
    
        if res:
            return [res]
        else:
            return []

class ActionAskMoreQuestion(Action):
    def name(self) -> Text:
        return "action_ask_more_question"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("Great! Do you have anymore questions?")
        return []


class ActionAnswerNotHelpful(Action):
    def name(self) -> Text:
        return "action_answer_not_helpful"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("I am sorry my answer is not helpful. I will be updated by the administator to answer this question better!")
        userAskedQuestion = tracker.get_slot(LAST_USER_QUESTION_ASKED)
        # This is the chatbotAnswer data model.
        answersProvidedByChatbot : List[Dict[str, any]]= tracker.get_slot(LAST_ANSWERS_PROVIDED_SLOT_NAME)

        for answer in answersProvidedByChatbot:
            answer["feedback"] = ""

        if answersProvidedByChatbot == None:
            answersProvidedByChatbot = []
        if not userAskedQuestion == None:
            addUnansweredQuestion(userAskedQuestion, answersProvidedByChatbot)

        return []


class ActionQueryKnowledgebase(Action):
    def name(self) -> Text:
        return "action_query_knowledgebase"

    def utterAppropriateAnswerWhenExceptionHappen(self, question, answers, exceptionReceived, dispatcher):
        try:
            exceptionType = exceptionReceived.type
            if exceptionType ==  ExceptionTypes.NoDataFoundAtAll:
                dispatcher.utter_message(text=str(exceptionReceived.fallBackMessage))
            else:
                utterAllAnswers(answers, dispatcher)
        except:
            # print(exceptionReceived)
            dispatcher.utter_message(
                "Sorry something went wrong, can you please ask again?")


    async def run(self, dispatcher, tracker, domain):
        startYear, endYear, setYearSlotEvent = None, None, None
        events =[]
        try:
            startYear, endYear, setYearSlotEvent = getYearRangeInSlot(tracker)
            if setYearSlotEvent:
                events.append(setYearSlotEvent)
        except:
            pass

        question = tracker.latest_message["text"]
        entitiesExtracted = tracker.latest_message["entities"]
        numberEntities = numberEntityExtractor.extractEntities(question)
        entitiesExtracted = entitiesExtracted + numberEntities
        intent = tracker.latest_message["intent"]["name"]

        print("INTENT")
        print(intent)
        print(getEntityLabel(removeDuplicatedEntities(entitiesExtracted)))
        print(getEntityValueHelper(removeDuplicatedEntities(entitiesExtracted)))
        print(entitiesExtracted)
        
        setLastIntentSlotEvent = SlotSet(LAST_TOPIC_INTENT_SLOT_NAME ,intent )
        events.append(setLastIntentSlotEvent)

        answers : List[ChatbotAnswer] = []
      
       
        for knowledgebase in knowledgebaseEnsemble:
            # try:
                newAnswers = await knowledgebase.searchForAnswer(question, intent, entitiesExtracted, startYear, endYear)
                answers = answers + newAnswers
            # except Exception as e:
            #     continue
            
            # divider = ["-------------------------"]
            
            # if len(answers)>0:
            #     break
        
        answerFromUnansweredQuestion = getAnswerForUnansweredQuestion(question)
        answers = answers + answerFromUnansweredQuestion
        print("ANSWERS", answers)
        if len(answers) <= 0:
            answers = [ChatbotAnswer("Sorry, I couldn't find any answer to your question", source="")]
            addUnansweredQuestion(question, answers)

        answers = checkIfAnswerFound(question, answers)
        event = utterAllAnswers(answers, dispatcher) 
        events.append(event)       

        # except Exception as e:
        #     if len(answers) <= 0:
        #         answers = ["Sorry, I couldn't find any answer to your question"]
        #         addUnansweredQuestion(question, answers)
                
        #     self.utterAppropriateAnswerWhenExceptionHappen(question, answers, e, dispatcher)
             
        return events

class ActionStoreAskedQuestion(Action):
    def name(self) -> Text:
        # return "action_store_asked_question_and_answer_provided"
        return "action_store_asked_question"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message["intent"]["name"]
        question = tracker.latest_message["text"]
        # print("STORING QUESTIOn", question
        event = SlotSet(LAST_USER_QUESTION_ASKED, question)
        intent = tracker.latest_message["intent"]["name"]
        data = {"intent": intent, "feedback": "NO_FEEDBACK", "content": question}
        # response = requests.put("http://127.0.0.1:8000/question_asked/", json=data)
        response = requests.put(BACKEND_API_URL+"/question_asked/", json=data)

        return [event]


class ActionStoreIsHelpfulStatistic(Action):
    def name(self) -> Text:
        return "action_store_isHelpful_statistic"
    
    def run(self, dispatcher, tracker, domain):
        #Get the stored question
        userAskedQuestion = tracker.get_slot(LAST_USER_QUESTION_ASKED)
        intent = tracker.latest_message["intent"]["name"]
        update_intent = "NO_FEEDBACK"
        if(intent == "deny"):
            update_intent = "NOT_HELPFUL"
        if(intent == "affirm"):
            update_intent = "HELPFUL"
        print(update_intent)
        data = {"intent": "UPDATE", "feedback": update_intent, "content": userAskedQuestion}
        #response = requests.put("http://127.0.0.1:8000/question_asked/", json=data)
        response = requests.put(BACKEND_API_URL+"/question_asked/", json=data)
        # print(userAskedQuestion)
        return []


class ActionGetYear(Action):
    def name(self) -> Text:
        return "action_get_year"
    
    def run(self, dispatcher, tracker, domain):
        yearRange = tracker.get_slot(YEAR_RANGE_SELECTED_SLOT_NAME )
        if yearRange == None:
            return []

        if len(yearRange) == 2:
            dispatcher.utter_message(yearRange[0])
            dispatcher.utter_message(yearRange[1])
        
        return []
        

class ActionSetYear(Action):
    def name(self) -> Text:
        return "action_set_year"
    
    def run(self, dispatcher, tracker, domain):
        # print("YEAR CHANGED")
        
        entitiesExtracted = tracker.latest_message["entities"]
        yearRange = []
        # Assume there are only two entities, the start year and end year
        for entities in entitiesExtracted:
            yearRange.append(entities["value"])
        res = SlotSet("yearRangeSelected", yearRange)
        return [res]


# class ActionNluFallback(Action):
#     def name(self) -> Text:
#         return "action_nlu_fallback"
    
#     def run(self, dispatcher, tracker, domain):
#         question = tracker.latest_message["text"]
#         answers = getAnswerForUnansweredQuestion(question)
#         answers = checkIfAnswerFound(question, answers)
#         utterAllAnswers(answers, dispatcher)



class ActionEventOccured(Action):
    def __init__(self) -> None:
        super().__init__()
        self.EVENT_TYPE_KEY = "eventType"

    def name(self) -> Text:
        return "action_event_occured"
    
    async def run(self, dispatcher, tracker, domain):
        entities = tracker.latest_message["entities"]
        eventTypeEntity = findEntityHelper(entities, self.EVENT_TYPE_KEY)

        if eventTypeEntity == None:
            return []
        
        eventType = eventTypeEntity["value"]
        trainingLabels : List[MultiFeedbackLabel] = []

        # determine what event to fire
        if eventType == "train":
            return self.handleTrainKnowledgebase(trainingLabels, entities, eventType)

        elif eventType == "dataUploaded":
            return await self.handleDataUpload(entities, eventType)
        
        elif eventType =="dataDeleted":
            return self.handleDataDelete(entities, eventType)
        
        return []


    async def handleDataUpload(self, entities, eventType):
        print(entities)
        dataNameEntity = findEntityHelper(entities, "dataName")
        startYearEntity = findEntityHelper(entities, "startYear")
        endYearEntity = findEntityHelper(entities, "endYear")

        startYear = None
        endYear = None
        if not startYearEntity == None and not endYearEntity == None:
            startYear = startYearEntity["value"]
            endYear = endYearEntity["value"]
        dataName = dataNameEntity["value"]

        for knowledgebase in knowledgebaseEnsemble:
           await knowledgebase.dataUploaded(dataName, startYear, endYear)

        return []

    def handleDataDelete(self, entities, eventType):
        dataNameEntity = findEntityHelper(entities, "dataName")
        dataName = dataNameEntity["value"]
        for knowledgebase in knowledgebaseEnsemble:
            knowledgebase.dataDeleted(dataName)

        return []


        
    def handleTrainKnowledgebase(self, trainingLabels, entities, eventType):
        """
        The feedback labels object looks like:
        {'entity': 'feedback', 'value': [ {'_id': {'$oid': '641b6117a799c3a9b43f72c1'},
        'content': 'How many faculty do you have at rose-hulman', 
        'post_date': {'$date': '2023-03-22T16:12:07.973Z'}, 
        'is_addressed': True, 
        'chatbotAnswers': [{answer:'the total number of instructional faculty is 192', source:"QuestionAnswerKnowledge", metadata:{}, feedback:"" }], 
        'answer': 'the total number of instructional faculty is 200'}} ] 
        """
        feedbackEntity= findEntityHelper(entities, "feedback")
        feedbackLabelsDict = feedbackEntity["value"]
        # convert to data model
        for data in feedbackLabelsDict:
            query = data["content"]
            feedbackLabels = []
            for chatbotAnswer in data["chatbotAnswers"]:
                source = chatbotAnswer["source"]
                metadata = chatbotAnswer["metadata"]
                feedback = chatbotAnswer["feedback"]
                answer = chatbotAnswer["answer"]
                if feedback == None or feedback == "":
                    continue
                if feedback == FeedbackType.CORRECT.value:
                    feedback = FeedbackType.CORRECT
                elif feedback == FeedbackType.INCORRECT.value:
                    feedback = FeedbackType.INCORRECT
                else: 
                    continue
                feedbackLabel = FeedbackLabel(query = query, source = source, metadata = metadata, feedback = feedback, answerProvided=answer)
                feedbackLabels.append(feedbackLabel)

            multiLabelFeedback = MultiFeedbackLabel(query=query,feedbackLabels= feedbackLabels)
            trainingLabels.append(multiLabelFeedback)

        for knowledgebase in knowledgebaseEnsemble:
            knowledgebase.train(trainingLabels)

        return [{"event": "action", "name": "action_event_occured", "eventType": eventType}]





# Helper functions
def checkIfAnswerFound(question, answers):
    if len(answers) <= 0:
        answers = [ChatbotAnswer("Sorry, I couldn't find any answer to your question", source="")]
        addUnansweredQuestion(question, answers)
    
    return answers

def getYearRangeInSlot(tracker):
    startYear, endYear = None, None
    yearRange = tracker.get_slot(YEAR_RANGE_SELECTED_SLOT_NAME )
    res = None
    if yearRange == None or len(yearRange) == 0:
        startYear, endYear = mongoDataManager.getMostRecentYearRange()
        if startYear and endYear:
            res = SlotSet(YEAR_RANGE_SELECTED_SLOT_NAME , [startYear, endYear] )
    else:
        startYear = yearRange[0]
        endYear = yearRange[1]
    
    return (startYear, endYear, res)


def utterAllAnswers(answers : List[ChatbotAnswer], dispatcher):
    print("ALL ANSWERS")
    print(answers)
    answersInDict = []
    for answer in answers:
        answerDict = answer.as_dict()
        answerDict["text"] = answerDict["answer"]
        # print("JSON MESSAGE",  {"answers": answerDict})
        answersInDict.append(answerDict)
        dispatcher.utter_message( json_message= answerDict)

    return SlotSet(LAST_ANSWERS_PROVIDED_SLOT_NAME, answersInDict)

def addUnansweredQuestion(question, chatbotAnswers): 
    data = {"content": question, "chatbotAnswers":chatbotAnswers}
    response = requests.post("http://127.0.0.1:8000/question_add/", json=data )

def getAnswerForUnansweredQuestion(question):
        response = requests.get(BACKEND_API_URL+"/answer_unanswered_question", params={"question": question})
        jsonData = response.json()
        answersKey = "answers"
        if answersKey in jsonData:
            answers = jsonData["answers"]
            chatbotAnswers = []
            for answer in answers:
                chatbotAnswer = ChatbotAnswer(question= question, answer= answer, source="unansweredQuestionEngine")
                chatbotAnswers.append(chatbotAnswer)
        
            return chatbotAnswers
           
        else:
            return []
        

