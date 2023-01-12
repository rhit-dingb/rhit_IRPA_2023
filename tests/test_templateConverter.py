
import unittest
from unittest import mock
from unittest.mock import patch
from DataManager.constants import AGGREGATION_ENTTIY_LABEL, INITIAL_COHORT_ENTITY_LABEL, NUMBER_ENTITY_LABEL, RANGE_ENTITY_LABEL, YEAR_ENTITY_LABEL

from OutputController.TemplateConverter import TemplateConverter
from Knowledgebase.DataModels.SearchResult import SearchResult
from tests.testUtils import checkAnswersMatch, createEntityObjHelper
from Knowledgebase.SearchResultType import SearchResultType
# These values are from student life in 2020-2021 CDS data

from actions.constants import AGGREGATION_ENTITY_AVERAGE_VALUE, AGGREGATION_ENTITY_PERCENTAGE_VALUE, RANGE_LOWER_BOUND_VALUE, RANGE_UPPER_BOUND_VALUE, STUDENT_ENROLLMENT_RESULT_ENTITY_GRADUATION_VALUE


class test_template_converter(unittest.TestCase):
   def setUp(self):
       self.testTemplate_1 = "The (xor [aggregation] number) of students {who graduated in [range] [number] years and [range] [number] years} in the [initial_final] [year] cohort is <value>"
       self.testTemplate_2 = "(xor {Hello} [aggregation])"
       self.badTemplate_3 = "(xor{Hello} done "
       self.complicatedTemplate = " (xor {On [*average], the [*percent] of financial need that was met for} {the number of}) degree-seeking, first-time, full-time freshman students (xor {whose need was [financial_aid_degree_met]} {who were awarded any [need_non_need_base_aid] [financial_aid_type] (xor [self-help] {scholarship and grant})}) aid is <value>"
       self.rangeTemplate = "(xor {[range] [number] and [number]} {[range] [number]})"
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

   def test_construct_output_for_range_template_should_return_correct_sentence(self):
        searchAnswers = ["5"]
        entitiesUsed = [[createEntityObjHelper("initial", entityLabel=INITIAL_COHORT_ENTITY_LABEL),
            createEntityObjHelper(RANGE_UPPER_BOUND_VALUE,
                                    entityLabel=RANGE_ENTITY_LABEL),
            createEntityObjHelper("6", entityLabel=NUMBER_ENTITY_LABEL),
            ]]

        searchResults = createSearchResult(searchAnswers, entitiesUsed)
        sentences = self.templateConverter.constructOutput(
        searchResults, self.rangeTemplate)
        print(sentences)
          
        answers = [
           "within 6"]
        checkAnswers(answers, sentences, self)


      
   def test_construct_output_for_template_1_should_return_correct_sentence(self):
       searchAnswers = ["5"]
       entitiesUsed = [[createEntityObjHelper("initial", entityLabel=INITIAL_COHORT_ENTITY_LABEL),
            createEntityObjHelper(RANGE_LOWER_BOUND_VALUE,
                                  entityLabel=RANGE_ENTITY_LABEL),
            createEntityObjHelper(RANGE_UPPER_BOUND_VALUE,
                                  entityLabel=RANGE_ENTITY_LABEL),
            createEntityObjHelper("5", entityLabel=NUMBER_ENTITY_LABEL),
            createEntityObjHelper("6", entityLabel=NUMBER_ENTITY_LABEL),
            createEntityObjHelper("2014", entityLabel=YEAR_ENTITY_LABEL)
            ]]

       searchResults = createSearchResult(searchAnswers, entitiesUsed)
       sentences = self.templateConverter.constructOutput(
           searchResults, self.testTemplate_1)
       answers = [
           "The number of students who graduated in more than 5 years and within 6 years in the initial 2014 cohort is 5"]
       checkAnswers(answers, sentences, self)

   def test_construct_output_for_template_2(self):
       searchAnswers = ["5"]

       entitiesUsed = [[
            createEntityObjHelper(
                AGGREGATION_ENTITY_PERCENTAGE_VALUE, entityLabel=AGGREGATION_ENTTIY_LABEL),
        ]]

       searchResults = createSearchResult(searchAnswers, entitiesUsed)
       sentences = self.templateConverter.constructOutput(
           searchResults, self.testTemplate_2)
       answers = ["Hello"]
       checkAnswers(answers, sentences, self)

   def test_construct_output_for_bad_template(self):
      searchAnswers = ["5"]
      entitiesUsed = [[
            createEntityObjHelper(
                AGGREGATION_ENTITY_PERCENTAGE_VALUE, entityLabel=AGGREGATION_ENTTIY_LABEL),
      ]]

      searchResults = createSearchResult(searchAnswers, entitiesUsed)
      self.assertRaises(Exception, self.templateConverter.constructOutput,
                        searchResults, self.badTemplate_3)

   def test_construct_output_for_complicated_template(self):
      searchAnswers = ["5"]
      entitiesUsed = [[
            createEntityObjHelper(
                AGGREGATION_ENTITY_PERCENTAGE_VALUE, entityLabel=AGGREGATION_ENTTIY_LABEL),
            createEntityObjHelper(
                AGGREGATION_ENTITY_AVERAGE_VALUE, entityLabel=AGGREGATION_ENTTIY_LABEL),

            createEntityObjHelper(
               "need-based", entityLabel= "need_non_need_base_aid"),
            createEntityObjHelper(
               "institutional", entityLabel= "financial_aid_type"),
      ]]

      searchResults = createSearchResult(searchAnswers, entitiesUsed)

      expectedAnswer = ["On average , the percent of financial need that was met for degree-seeking, first-time, full-time freshman students who were awarded any need-based institutional scholarship and grant aid is 5"]
      sentences= self.templateConverter.constructOutput(searchResults, self.complicatedTemplate)
      checkAnswers(expectedAnswer, sentences, self)
      print(sentences)


def checkAnswers(sentences, answers, unitTest):
    for i in range(len(sentences)):
        unitTest.assertEqual(answers[i], sentences[i])


def createSearchResult(searchAnswers, entitiesUsed):
    searchResults = []
    for answer, entities in zip(searchAnswers, entitiesUsed):
            #  answer, entitiesUsed : List[Dict[str, str]], type : SearchResultType, realQuestion : str
        searchResult = SearchResult(answer, entities, SearchResultType.STRING, [] )
        searchResults.append(searchResult)

    return searchResults


if __name__ == '__main__':
    unittest.main()
