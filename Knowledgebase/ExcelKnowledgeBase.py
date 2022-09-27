
from Knowledgebase.Knowledgebase import KnowledgeBase
from Knowledgebase.LevenshteinMatcher import LevenshteinMatcher
import pandas as pd

class ExcelKnowledgeBase(KnowledgeBase):
    def __init__(self, filePath):
        self.filePath = filePath
        self.xl = pd.ExcelFile(filePath)
        self.data = dict()
        self.processExcel()
        #use this matcher for now, if it is not doing too good we can swap it out.
        self.matcher = LevenshteinMatcher()

    def initialize():
      pass


    def getAvailableOptions(self, key):
       pass

    def searchForAnswer(self, intent, entities):
      #Algorithm to search in knowledgebase for answers:
      #For each possible sheet of given intent
      #Use matcher - first check if anything match, if so, drill down, remove that entity
      #In the new drill downed part, check for anything match, if so drill down. If not, get the total of the rest of key. 

      # this is very simplistic search code and not completed yet. 
      if intent.lower() not in self.data:
        raise Exception("The intent provided has no data associated with it")
      else:
        data = self.data[intent]
        while len(entities) > 0:
          match = self.matcher.match(entities, data.keys())
          print(match)
          entities.remove(match[1])
          keyToGoInto = match[0]
          data = data[keyToGoInto]

      return data


    def processExcel(self):

        enrollmentSubColumns = pd.MultiIndex.from_product([['Full-Time','Part-time'], ["Men", "Woman"]])
        for name in self.xl.sheet_names: 
            df = self.xl.parse(name)
           
            topic_key_words = [x.lower() for x in name.split(" ")]
            #only parse enrollment for now
            #print(topic_key_words)
            if("enrollment" in topic_key_words):
              ## get the top left value of the excel--this value specifies undergradudate or graduate for enrollment
          
              subName = df.columns[0]
              df = df.set_index(subName)
              index = df.index
              data = df.values
            
              # convert to multi index dataframe for full-time and gender
              df = pd.DataFrame(data, columns=enrollmentSubColumns, index = index)
              df = self.df_to_nested_dict(df)
      
              if ("enrollment" in self.data): 
                enrollmentData = self.data["enrollment"]
                enrollmentData[subName.lower()] = df
               
              else:
                newDf = dict()
                newDf[subName.lower()] = df
                self.data["enrollment"] = newDf
      


    #helper to convert enrollment data to json format, represented by python dictionary.
    def df_to_nested_dict(self, df: pd.DataFrame) -> dict:
        d = df.to_dict(orient='index')
        return {k: self.nest(v) for k, v in d.items()}

    def nest(self, dataInDictionaryFormat):
        result = {}
        for key, value in dataInDictionaryFormat.items():
            target = result
            #print(key[:-1])
            for k in key[:-1]:# traverse all keys but the last
                # will return the reference to the dictionary we passed in as value for k. 
                target = target.setdefault(k, {})
                
            #put in final key in along with the value
            target[key[-1]] = value
            
        return result
