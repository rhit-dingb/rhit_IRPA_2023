
import json
import unittest
from unittest.mock import patch
from DataManager.constants import *
from Exceptions.ExceptionMessages import NO_DATA_FOUND_FOR_COHORT_YEAR_ERROR_MESSAGE_FORMAT
from Knowledgebase.Knowledgebase import KnowledgeBase

from Knowledgebase.SparseMatrixKnowledgeBase import SparseMatrixKnowledgeBase
from Knowledgebase.DefaultShouldAddRow import DefaultShouldAddRowStrategy
from DataManager.ExcelDataManager import ExcelDataManager
from OutputController import output
from actions.constants import AGGREGATION_ENTITY_PERCENTAGE_VALUE, RANGE_LOWER_BOUND_VALUE, RANGE_UPPER_BOUND_VALUE, STUDENT_ENROLLMENT_RESULT_ENTITY_GRADUATION_VALUE, YEARS_FOR_COLLEGE_ENTITY_FORMAT
from tests.testUtils import checkAnswersMatch, createEntityObjHelper, createFakeTracker, identityFunc
from actions.actions import knowledgeBase as knowledgeBaseInAction
from actions.actions import ActionQueryCohort

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

#These values are from the 2014 cohort in the 2013-2014 dataset 
INITIAL_2014_COHORT_TOTAL = 582
FINAL_2014_COHORT = 581
COHORT_2014_STUDENT_GRADUATING_IN_MORE_THAN_4_YEARS_AND_IN_FIVE_OR_LESS = 49

COHORT_2014_STUDENT_GRADUATING_IN_MORE_THAN_5_YEARS_AND_IN_6_OR_LESS = 9

COHORT_2014_SIX_YEAR_GRADUATED_STUDENTS = 483
COHORT_2014_SIX_YEAR_STUDENT_GRADUATION_RATE = "83.1%"
COHORT_2014_FIVE_YEAR_STUDENT_GRADUATION_RATE = "81.6%"
COHORT_2014_FOUR_YEAR_STUDENT_GRADUATION_RATE = "73.1%"
COHORT_2014_FOUR_YEAR_GRADUATED_STUDENT_RECEIVED_PELL_GRANT = 61
COHORT_2014_STUDENT_GRADUATED_FOUR_TO_FIVE_YEAR_RECEIVED_STAFFORD_LOAN = 9
COHORT_2014_STUDENT_GRADUATED_IN_MORE_THAN_FIVE_YEARS_WHO_RECEIVED_NO_AID = 36
COHORT_2014_STUDENT_GRADUATED_FIVE_TO_SIX_YEAR_WHO_RECEIVED_STAFFORD_LOAN = 5
COHORT_2014_STUDENT_RECEIVED_STAFFORD_LOAN = 199
class Cohort_Test(unittest.TestCase):
    def setUp(self):
        self.topicToParse = ["enrollment", "cohort"]
        self.knowledgeBase = SparseMatrixKnowledgeBase(
            ExcelDataManager("./tests/testMaterials", self.topicToParse))

        
        self.defaultShouldAddRowStrategy = DefaultShouldAddRowStrategy()


        self.dispatcher = CollectingDispatcher()
        #Make sure the knowledgebase class instance in Actions is using the data manager with test materials loaded.
        knowledgeBaseInAction.dataManager = self.knowledgeBase.dataManager
        knowledgeBaseInAction.constructOutput = identityFunc
        #self.patcher = mock.patch("OutputController.output.constructSentence", return_value = )
        

    #Cohorts actually uses the label of the entities, so we have to write test cases in terms of actions.
    def test_knowledgebase_when_ask_for_initial_cohort_should_return_correct_value(self):
            answers = self.knowledgeBase.searchForAnswer(
                "cohort",
                [
                createEntityObjHelper("initial"),
                createEntityObjHelper("2014 cohort", entityLabel=COHORT_BY_YEAR_ENTITY_LABEL)
                ], self.defaultShouldAddRowStrategy, output.constructSentence
            )
            expectedAnswers = [str(INITIAL_2014_COHORT_TOTAL)]
            self.assertEqual(answers, expectedAnswers)

    def test_when_ask_only_for_graduation_rate_should_return_six_year_graduation_rate(self):
        entities = [
            createEntityObjHelper("initial"),
            createEntityObjHelper("2014 cohort", entityLabel=COHORT_BY_YEAR_ENTITY_LABEL),
             
        ]

    def test_when_ask_for_graduation_time_five_to_six_year_should_give_correct_value_for_action(self):
        entities =  [
            createEntityObjHelper("initial", entityLabel=INITIAL_COHORT_ENTITY_LABEL),
            createEntityObjHelper("2014 cohort", entityLabel=COHORT_BY_YEAR_ENTITY_LABEL),
            createEntityObjHelper(RANGE_LOWER_BOUND_VALUE, entityLabel= RANGE_ENTITY_LABEL),
            createEntityObjHelper(RANGE_UPPER_BOUND_VALUE, entityLabel= RANGE_ENTITY_LABEL),
            createEntityObjHelper(YEARS_FOR_COLLEGE_ENTITY_FORMAT.format(year = "5"), entityLabel= YEAR_FOR_COLLEGE_ENTITY_LABEL ),
            createEntityObjHelper(YEARS_FOR_COLLEGE_ENTITY_FORMAT.format(year="6"),
                                  entityLabel=YEAR_FOR_COLLEGE_ENTITY_LABEL)
            ]

        print(entities)
        knowledgeBaseInAction.dataManager = self.knowledgeBase.dataManager
        queryCohort = ActionQueryCohort()
     
        tracker = Tracker.from_dict(createFakeTracker(COHORT_INTENT, entities))
        queryCohort.run(dispatcher=self.dispatcher, tracker=tracker, domain=None )
        expectedAnswers = [str(COHORT_2014_STUDENT_GRADUATING_IN_MORE_THAN_5_YEARS_AND_IN_6_OR_LESS)]
        checkAnswersMatch(self.assertEqual, self.dispatcher, expectedAnswers)

   
   
    def test_when_ask_for_final_cohort_should_give_correct_value_for_action(self):
        entities =  [
            createEntityObjHelper(FINAL_COHORT_ENTITY_LABEL, entityLabel=FINAL_COHORT_ENTITY_LABEL),
            createEntityObjHelper("2014 cohort", entityLabel=COHORT_BY_YEAR_ENTITY_LABEL),
        ]
            
        knowledgeBaseInAction.dataManager = self.knowledgeBase.dataManager
        queryCohort = ActionQueryCohort()
        tracker = Tracker.from_dict(createFakeTracker(COHORT_INTENT, entities))
        queryCohort.run(dispatcher=self.dispatcher, tracker=tracker, domain=None )
        expectedAnswers = [str(FINAL_2014_COHORT)]
        checkAnswersMatch(self.assertEqual, self.dispatcher, expectedAnswers)

    def test_when_ask_for_six_year_graduation_rate_should_give_correct_value_for_action(self):
        entities =  [
            createEntityObjHelper("2014 cohort", entityLabel=COHORT_BY_YEAR_ENTITY_LABEL),
            createEntityObjHelper(YEARS_FOR_COLLEGE_ENTITY_FORMAT.format(year="6"),
                                  entityLabel=YEAR_FOR_COLLEGE_ENTITY_LABEL),
            createEntityObjHelper(RANGE_UPPER_BOUND_VALUE, entityLabel= RANGE_ENTITY_LABEL),
            createEntityObjHelper(STUDENT_ENROLLMENT_RESULT_ENTITY_GRADUATION_VALUE, entityLabel=STUDENT_ENROLLMENT_RESULT_ENTITY_LABEL),
            createEntityObjHelper(AGGREGATION_ENTITY_PERCENTAGE_VALUE, entityLabel=AGGREGATION_ENTTIY_LABEL )
            ]
            

        queryCohort = ActionQueryCohort()
        tracker = Tracker.from_dict(createFakeTracker(COHORT_INTENT, entities))
        queryCohort.run(dispatcher=self.dispatcher, tracker=tracker, domain=None )
        # print(dispatcher.messages[0]["text"])
        expectedAnswers = [COHORT_2014_SIX_YEAR_STUDENT_GRADUATION_RATE]
        checkAnswersMatch(self.assertEqual, self.dispatcher, expectedAnswers) 

    def test_when_ask_for_five_year_graduation_rate_should_give_correct_value_for_action(self):
        entities =  [
            createEntityObjHelper("2014 cohort", entityLabel=COHORT_BY_YEAR_ENTITY_LABEL),
            createEntityObjHelper(YEARS_FOR_COLLEGE_ENTITY_FORMAT.format(year="5"),
                                  entityLabel=YEAR_FOR_COLLEGE_ENTITY_LABEL),
            createEntityObjHelper(RANGE_UPPER_BOUND_VALUE, entityLabel= RANGE_ENTITY_LABEL),
            createEntityObjHelper(STUDENT_ENROLLMENT_RESULT_ENTITY_GRADUATION_VALUE, entityLabel=STUDENT_ENROLLMENT_RESULT_ENTITY_LABEL),
            createEntityObjHelper(AGGREGATION_ENTITY_PERCENTAGE_VALUE, entityLabel=AGGREGATION_ENTTIY_LABEL )

            ]
            
        knowledgeBaseInAction.dataManager = self.knowledgeBase.dataManager
        queryCohort = ActionQueryCohort()
   
        tracker = Tracker.from_dict(createFakeTracker(COHORT_INTENT, entities))
        queryCohort.run(dispatcher=self.dispatcher, tracker=tracker, domain=None )
        expectedAnswers = [COHORT_2014_FIVE_YEAR_STUDENT_GRADUATION_RATE]
        checkAnswersMatch(self.assertEqual, self.dispatcher, expectedAnswers) 

    def test_when_ask_for_four_year_graduation_rate_should_give_correct_value_for_action(self):
        entities =  [
            createEntityObjHelper("2014 cohort", entityLabel=COHORT_BY_YEAR_ENTITY_LABEL),
            createEntityObjHelper(YEARS_FOR_COLLEGE_ENTITY_FORMAT.format(year="4"),
                                  entityLabel=YEAR_FOR_COLLEGE_ENTITY_LABEL),
            createEntityObjHelper(RANGE_UPPER_BOUND_VALUE, entityLabel= RANGE_ENTITY_LABEL),
            createEntityObjHelper(STUDENT_ENROLLMENT_RESULT_ENTITY_GRADUATION_VALUE, entityLabel=STUDENT_ENROLLMENT_RESULT_ENTITY_LABEL),
            createEntityObjHelper(AGGREGATION_ENTITY_PERCENTAGE_VALUE, entityLabel=AGGREGATION_ENTTIY_LABEL )
            ]
            
        queryCohort = ActionQueryCohort()
        tracker = Tracker.from_dict(createFakeTracker(COHORT_INTENT, entities))
        queryCohort.run(dispatcher=self.dispatcher, tracker=tracker, domain=None )
        expectedAnswers = [COHORT_2014_FOUR_YEAR_STUDENT_GRADUATION_RATE]
        checkAnswersMatch(self.assertEqual, self.dispatcher, expectedAnswers) 


    def test_when_ask_for_invalid_cohort_year_should_return_exception_message(self):
        entities =  [
            createEntityObjHelper("3952 cohort", entityLabel=COHORT_BY_YEAR_ENTITY_LABEL),
            createEntityObjHelper("exemptions", entityLabel=EXEMPTION_ENTITY_LABEL),
        ]
        
        knowledgeBaseInAction.dataManager = self.knowledgeBase.dataManager
        queryCohort = ActionQueryCohort()
        tracker = Tracker.from_dict(createFakeTracker(COHORT_INTENT, entities))
        queryCohort.run(dispatcher=self.dispatcher, tracker=tracker, domain=None )
        expectedAnswers = [NO_DATA_FOUND_FOR_COHORT_YEAR_ERROR_MESSAGE_FORMAT.format(year = 3952)]
        checkAnswersMatch(self.assertEqual, self.dispatcher, expectedAnswers) 

    def test_when_ask_for_cohort_given_invalid_year_and_upper_bound(self):
        entities =  [
            createEntityObjHelper("3952 cohort", entityLabel=COHORT_BY_YEAR_ENTITY_LABEL),
            createEntityObjHelper(YEARS_FOR_COLLEGE_ENTITY_FORMAT.format(year="7"), entityLabel=YEAR_FOR_COLLEGE_ENTITY_LABEL),
            createEntityObjHelper(RANGE_UPPER_BOUND_VALUE, entityLabel= RANGE_ENTITY_LABEL)
        ]
            
        queryCohort = ActionQueryCohort()
        tracker = Tracker.from_dict(createFakeTracker(COHORT_INTENT, entities))
        queryCohort.run(dispatcher=self.dispatcher, tracker=tracker, domain=None )
        expectedAnswers = [NO_DATA_FOUND_FOR_COHORT_YEAR_ERROR_MESSAGE_FORMAT.format(year = 3952)]
        checkAnswersMatch(self.assertEqual, self.dispatcher, expectedAnswers) 

    def test_when_ask_for_cohort_given_invalid_lower_bound__for_graduation_time_should_return_six_year_graduation_number(self):
        entities =  [
            createEntityObjHelper("2014 cohort", entityLabel=COHORT_BY_YEAR_ENTITY_LABEL),
            createEntityObjHelper(YEARS_FOR_COLLEGE_ENTITY_FORMAT.format(year="89999"), entityLabel=YEAR_FOR_COLLEGE_ENTITY_LABEL),
            createEntityObjHelper(RANGE_LOWER_BOUND_VALUE, entityLabel= RANGE_ENTITY_LABEL),

        ]
            
        queryCohort = ActionQueryCohort()
        tracker = Tracker.from_dict(createFakeTracker(COHORT_INTENT, entities))
        queryCohort.run(dispatcher=self.dispatcher, tracker=tracker, domain=None )
        expectedAnswers = [str(COHORT_2014_SIX_YEAR_GRADUATED_STUDENTS)]
        checkAnswersMatch(self.assertEqual, self.dispatcher, expectedAnswers) 

    # def test_when_ask_for_students_graduating_within_4_years_who_received_pell_grant_should_return_correct_value(self):
    #     entities =  [
    #         createEntityObjHelper("2014 cohort", entityLabel=COHORT_BY_YEAR_ENTITY_LABEL),
    #         createEntityObjHelper("4 years or less", entityLabel=UPPER_BOUND_GRADUATION_TIME_ENTITY_LABEL),
    #         createEntityObjHelper("pell-grant", entityLabel="recipients_of_pell_grant"),
    #     ]
            
    #     queryCohort = ActionQueryCohort()
    #     tracker = Tracker.from_dict(createFakeTracker(COHORT_INTENT, entities))
    #     queryCohort.run(dispatcher=self.dispatcher, tracker=tracker, domain=None )
    #     self.assertEqual(self.dispatcher.messages[0]["text"], str(COHORT_2014_FOUR_YEAR_GRADUATED_STUDENT_RECEIVED_PELL_GRANT))

    # def test_when_ask_for_students_graduating_within_4_to_5_years_who_received_subsidized_loan_should_return_correct_value(self):
    #     entities =  [
    #         createEntityObjHelper("2014 cohort", entityLabel=COHORT_BY_YEAR_ENTITY_LABEL),
    #         createEntityObjHelper("5 years or less", entityLabel=UPPER_BOUND_GRADUATION_TIME_ENTITY_LABEL),
    #         createEntityObjHelper("more than 4 years", entityLabel=LOWER_BOUND_GRADUATION_TIME_ENTITY_LABEL),
    #         createEntityObjHelper("stafford-loan", entityLabel="recipients_of_a_subsidized_stafford_loan_who_did_not_receive_a_pell_grant"),
    #     ]
            
    #     queryCohort = ActionQueryCohort()
    #     tracker = Tracker.from_dict(createFakeTracker(COHORT_INTENT, entities))
    #     queryCohort.run(dispatcher=self.dispatcher, tracker=tracker, domain=None )
    #     self.assertEqual(self.dispatcher.messages[0]["text"], str(COHORT_2014_STUDENT_GRADUATED_FOUR_TO_FIVE_YEAR_RECEIVED_STAFFORD_LOAN))

    # def test_when_ask_for_students_graduating_within_4_years_as_lower_bound_who_no_aid_return_correct_value(self):
    #     entities =  [
    #         createEntityObjHelper("2014 cohort", entityLabel=COHORT_BY_YEAR_ENTITY_LABEL),
    #         createEntityObjHelper("more than 4 years", entityLabel=LOWER_BOUND_GRADUATION_TIME_ENTITY_LABEL),
    #         createEntityObjHelper("no-aid", entityLabel="students_who_did_not_receive_either_a_pell_grant_or_a_subsidized_stafford_loan"),
    #     ]
            
    #     queryCohort = ActionQueryCohort()
    #     tracker = Tracker.from_dict(createFakeTracker(COHORT_INTENT, entities))
    #     queryCohort.run(dispatcher=self.dispatcher, tracker=tracker, domain=None )
    #     self.assertEqual(self.dispatcher.messages[0]["text"], str(COHORT_2014_STUDENT_GRADUATED_IN_MORE_THAN_FIVE_YEARS_WHO_RECEIVED_NO_AID))

    # def test_when_ask_for_students_graduating_within_5_to_years_who_received_subsidized_loan_should_return_correct_value(self):
    #     entities =  [
    #         createEntityObjHelper("2014 cohort", entityLabel=COHORT_BY_YEAR_ENTITY_LABEL),
    #         createEntityObjHelper("6 years or less", entityLabel=UPPER_BOUND_GRADUATION_TIME_ENTITY_LABEL),
    #         createEntityObjHelper("more than 5 years", entityLabel=LOWER_BOUND_GRADUATION_TIME_ENTITY_LABEL),
    #         createEntityObjHelper("stafford-loan", entityLabel="recipients_of_a_subsidized_stafford_loan_who_did_not_receive_a_pell_grant"),
    #     ]
            
    #     queryCohort = ActionQueryCohort()
    #     tracker = Tracker.from_dict(createFakeTracker(COHORT_INTENT, entities))
    #     queryCohort.run(dispatcher=self.dispatcher, tracker=tracker, domain=None )
    #     self.assertEqual(self.dispatcher.messages[0]["text"], str(COHORT_2014_STUDENT_GRADUATED_FIVE_TO_SIX_YEAR_WHO_RECEIVED_STAFFORD_LOAN))

    # def test_when_ask_for_students_who_received_subsidized_loan_should_return_correct_value(self):
    #     entities =  [
    #         createEntityObjHelper("2014 cohort", entityLabel=COHORT_BY_YEAR_ENTITY_LABEL),
    #         createEntityObjHelper("some random value for stafford loan", entityLabel="recipients_of_a_subsidized_stafford_loan_who_did_not_receive_a_pell_grant"),
    #     ]
            
    #     queryCohort = ActionQueryCohort()
    #     tracker = Tracker.from_dict(createFakeTracker(COHORT_INTENT, entities))
    #     queryCohort.run(dispatcher=self.dispatcher, tracker=tracker, domain=None )
    #     self.assertEqual(self.dispatcher.messages[0]["text"], str(COHORT_2014_STUDENT_RECEIVED_STAFFORD_LOAN))


    # def test_when_ask_for_students_who_received_no_aid_should_return_correct_value(self):
    #     entities =  [
    #         createEntityObjHelper("2014 cohort", entityLabel=COHORT_BY_YEAR_ENTITY_LABEL),
    #         createEntityObjHelper("final", entityLabel=FINAL_COHORT_ENTITY_LABEL),
    #         createEntityObjHelper("student received no aid", entityLabel=NO_AID_ENTITY_LABEL),
    #     ]
            
    #     queryCohort = ActionQueryCohort()
    #     tracker = Tracker.from_dict(createFakeTracker(COHORT_INTENT, entities))
    #     queryCohort.run(dispatcher=self.dispatcher, tracker=tracker, domain=None )
    #     self.assertEqual(self.dispatcher.messages[0]["text"], str(299))

if __name__ == '__main__':
    unittest.main()
