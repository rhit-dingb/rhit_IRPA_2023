import re
import string
from word2number import w2n
from Knowledgebase.SearchResultType import SearchResultType

from Knowledgebase.TypeController import TypeController
from actions.entititesHelper import createEntityObj, findCharIndexForWord
class NumberEntityExtractor():
    def __init__(self):
        self.typeController = TypeController()

    def extractEntities(self, text):
        text = text.replace("-", " ")
        words = text.split(" ")
      
        text = " ".join(words)
        # #Replace punctuation
        text = text.translate(str.maketrans('', '', string.punctuation.replace(".", "")))
        numWordString = ""
        # Replace period
        text = re.sub(r'\.$', '', text)
        words =text.split(" ")
        entities = []
       
       
        convertedToNumberSuccess = False
        
        for word in words:
            castedWord, wordType = self.typeController.determineResultType(word)
            if wordType == SearchResultType.STRING :
                canConvert = not numWordString == "" and convertedToNumberSuccess
               
                try:
                    number = w2n.word_to_num(word)
                    if canConvert:
                        currentNumber = w2n.word_to_num(numWordString)
                        if currentNumber%10 == currentNumber:
                            entity = self.createEntity(number,word ,text)
                            entities.append(entity)
                            continue

                    numWordString = numWordString +" "+ word
                    convertedToNumberSuccess = True
                except Exception:
                    if canConvert:
                        number = str(w2n.word_to_num(numWordString))
                       
                        entity = self.createEntity(number,word ,text)
                        numWordString = ""
                        convertedToNumberSuccess = False
                        entities.append(entity)
                        
            elif wordType == SearchResultType.NUMBER or wordType == SearchResultType.FLOAT:
                print(castedWord)
                entity = self.createEntity(word,word, text)
                entities.append(entity)

        return entities



    def createEntity(self,value, originalValue, text):
        entity = createEntityObj(value, entityLabel="number",  entityRole=None)
        entity["extractor"] = "custom"
        entity["processors"] = []
        entity["confidence"] = 1.0
        start, end = findCharIndexForWord(originalValue, text)
        entity["start"] = start
        entity["end"] = end
        return entity


