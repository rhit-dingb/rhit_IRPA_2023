# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


import asyncio
import requests



from CustomEntityExtractor.NumberEntityExtractor import NumberEntityExtractor
from DataManager.ExcelDataManager import ExcelDataManager
from DataManager.constants import  COHORT_BY_YEAR_ENTITY_LABEL, COHORT_INTENT, ENROLLMENT_INTENT, EXEMPTION_ENTITY_LABEL, FRESHMAN_PROFILE_INTENT, HIGH_SCHOOL_UNITS_INTENT, INITIAL_COHORT_ENTITY_LABEL,  AID_ENTITY_LABEL, NO_AID_ENTITY_LABEL, RANGE_ENTITY_LABEL, RECIPIENT_OF_PELL_GRANT_ENTITY_LABEL, RECIPIENT_OF_STAFFORD_LOAN_NO_PELL_GRANT_ENTITY_LABEL, STUDENT_LIFE_INTENT, TRANSFER_ADMISSION_INTENT, YEAR_FOR_COLLEGE_ENTITY_LABEL
from Exceptions.ExceptionTypes import ExceptionTypes
from Knowledgebase.DefaultShouldAddRow import DefaultShouldAddRowStrategy

from Knowledgebase.IgnoreRowPiece import IgnoreRowPiece
from Knowledgebase.SparseMatrixKnowledgeBase import SparseMatrixKnowledgeBase
from OutputController import output

from actions.constants import  LAST_ANSWERS_PROVIDED_SLOT_NAME, YEAR_RANGE_SELECTED_SLOT_NAME, AGGREGATION_ENTITY_PERCENTAGE_VALUE, ANY_AID_COLUMN_NAME, NO_AID_COLUMN_NAME, PELL_GRANT_COLUMN_NAME, RANGE_BETWEEN_VALUE, RANGE_UPPER_BOUND_VALUE, STAFFORD_LOAN_COLUMN_NAME, STUDENT_ENROLLMENT_RESULT_ENTITY_GRADUATION_VALUE
from actions.entititesHelper import changeEntityValue, changeEntityValueByRole, copyEntities, createEntityObj, filterEntities, findEntityHelper, findMultipleSameEntitiesHelper, getEntityLabel, getEntityValueHelper, removeDuplicatedEntities
from typing import Text
from DataManager.MongoDataManager import MongoDataManager
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from actions.ResponseType import ResponseType
from actions.constants import LAST_TOPIC_INTENT_SLOT_NAME, LAST_USER_QUESTION_ASKED
import backendAPI.general_api  as API 


# ExcelDataManager("./CDSData", [ENROLLMENT_INTENT, COHORT_INTENT, ADMISSION_INTENT, HIGH_SCHOOL_UNITS_INTENT, BASIS_FOR_SELECTION_INTENT, FRESHMAN_PROFILE_INTENT, TRANSFER_ADMISSION_INTENT, STUDENT_LIFE_INTENT])
mongoDataManager = MongoDataManager()
knowledgeBase = SparseMatrixKnowledgeBase(mongoDataManager)
numberEntityExtractor = NumberEntityExtractor()


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
        answersProvidedByChatbot = tracker.get_slot(LAST_ANSWERS_PROVIDED_SLOT_NAME)
        
        # print("ANSWER PROVIDED")
        # print(answersProvidedByChatbot)
        if answersProvidedByChatbot == None:
            answersProvidedByChatbot = []
        if not userAskedQuestion == None:
            addUnansweredQuestion(userAskedQuestion, answersProvidedByChatbot)

        return []




class ActionQueryKnowledgebase(Action):
    def name(self) -> Text:
        return "action_query_knowledgebase"

    def getAnswerForUnansweredQuestion(self,question):
    
        answersFromUnansweredQuestion = API.unansweredQuestionAnswerEngine.answerQuestion(question)  
        return answersFromUnansweredQuestion

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

        answers = []
      
        # try:
        defaultShouldAddRowStrategy = DefaultShouldAddRowStrategy()
        answers = await knowledgeBase.searchForAnswer(intent, entitiesExtracted, defaultShouldAddRowStrategy,knowledgeBase.constructOutput,startYear, endYear )
        answerFromUnansweredQuestion = self.getAnswerForUnansweredQuestion(question)
        # print("ANSWER FOUND")
        # print(answerFromUnansweredQuestion)

        answers = answers + answerFromUnansweredQuestion
        if len(answers) <= 0:
            answers = ["Sorry, I couldn't find any answer to your question"]
            addUnansweredQuestion(question, answers)
        
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
        response = requests.put("http://127.0.0.1:8000/question_asked/", json=data)

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
        response = requests.put("http://127.0.0.1:8000/question_asked/", json=data)
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
        dispatcher.utter_message("Sorry, Cohort queries are not currently supported.")
        return 
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


def getYearRangeInSlot(tracker):
    startYear, endYear = None, None
    yearRange = tracker.get_slot(YEAR_RANGE_SELECTED_SLOT_NAME )
    # print("YEAR RANGE FOUND")
    # print(yearRange)
    res = None
    if yearRange == None or len(yearRange) == 0:
        startYear, endYear = mongoDataManager.getMostRecentYearRange()
        if startYear and endYear:
            res = SlotSet(YEAR_RANGE_SELECTED_SLOT_NAME , [startYear, endYear] )
    else:
        startYear = yearRange[0]
        endYear = yearRange[1]
    
    return (startYear, endYear, res)


def utterAllAnswers(answers, dispatcher ):
    # json_str = json.dumps(json_message)
    for answer in answers:
        dispatcher.utter_message( json_message={"text":answer} )

    return SlotSet(LAST_ANSWERS_PROVIDED_SLOT_NAME, answers)

def addUnansweredQuestion(question, chatbotAnswers): 
    data = {"content": question, "chatbotAnswers":chatbotAnswers}
    response = requests.post("http://127.0.0.1:8000/question_add/", json=data )
    