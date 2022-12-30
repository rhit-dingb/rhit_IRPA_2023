
import unittest
from unittest import mock
from unittest.mock import patch
from DataManager.constants import AGGREGATION_ENTTIY_LABEL, INITIAL_COHORT_ENTITY_LABEL, NUMBER_ENTITY_LABEL, RANGE_ENTITY_LABEL, YEAR_ENTITY_LABEL

from OutputController.TemplateConverter import TemplateConverter
from tests.testUtils import checkAnswersMatch, createEntityObjHelper
#These values are from student life in 2020-2021 CDS data

from actions.constants import AGGREGATION_ENTITY_PERCENTAGE_VALUE, RANGE_LOWER_BOUND_VALUE, RANGE_UPPER_BOUND_VALUE, STUDENT_ENROLLMENT_RESULT_ENTITY_GRADUATION_VALUE

class test_template_converter(unittest.TestCase):
    def setUp(self):
       self.testTemplate_1 = "The (xor [aggregation] number) of students {who graduated in [range] [number] years and [range] [number] years} in the [initial_final] [year] cohort is <value>"
       self.testTemplate_2 = "(xor {Hello} [aggregation])"
       self.badTemplate_3 = "(xor{Hello} done "
       self.templateConverter = TemplateConverter()
              
    # def test_parse_template_for_entity_expression(self):
    #    expressions = self.templateConverter.parseTemplate(self.testTemplate_1)
    #    print(expressions)
    #    for expression in expressions:
    #         print(expression.value)
    #         if len(expression.childrenExpression) > 0:
    #             print("PRINTING CHILDREN-------")
    #             for exp in expression.childrenExpression:
    #                 print(exp.value)
    #             print("-------------")
    
    def test_construct_output_for_template_1_should_return_correct_sentence(self):
       searchAnswers = ["5"]
       entitiesUsed =  [createEntityObjHelper("initial", entityLabel=INITIAL_COHORT_ENTITY_LABEL),
            createEntityObjHelper(RANGE_LOWER_BOUND_VALUE, entityLabel= RANGE_ENTITY_LABEL),
            createEntityObjHelper(RANGE_UPPER_BOUND_VALUE, entityLabel= RANGE_ENTITY_LABEL),
            createEntityObjHelper("5", entityLabel= NUMBER_ENTITY_LABEL ),
            createEntityObjHelper("6",entityLabel=NUMBER_ENTITY_LABEL),
            createEntityObjHelper("2014", entityLabel = YEAR_ENTITY_LABEL)
            ]

      
       sentences = self.templateConverter.constructOutput(searchAnswers, entitiesUsed, self.testTemplate_1)
       answers = ["The number of students who graduated in more than 5 years and within 6 years in the initial 2014 cohort is 5"]
       checkAnswers(answers, sentences, self)

    def test_construct_output_for_template_2(self):
       searchAnswers = ["5"]

       entitiesUsed =  [
            createEntityObjHelper(AGGREGATION_ENTITY_PERCENTAGE_VALUE, entityLabel= AGGREGATION_ENTTIY_LABEL),
        ]

      
       sentences = self.templateConverter.constructOutput(searchAnswers, entitiesUsed, self.testTemplate_2)
       answers = ["Hello"]
       checkAnswers(answers, sentences, self)

    def test_construct_output_for_bad_template(self):
       searchAnswers = ["5"]
       entitiesUsed =  [
            createEntityObjHelper(AGGREGATION_ENTITY_PERCENTAGE_VALUE, entityLabel= AGGREGATION_ENTTIY_LABEL),
        ]

       self.assertRaises(Exception, self.templateConverter.constructOutput, searchAnswers, entitiesUsed, self.badTemplate_3)
    

def checkAnswers(sentences, answers, unitTest):
    for i in range(len(sentences)):
        unitTest.assertEqual(answers[i], sentences[i])

if __name__ == '__main__':
    unittest.main()
