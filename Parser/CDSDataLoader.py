
# Interface to load and process the new data that the client would upload annually.
from Parser import QuestionAnswer
from typing import List


#The purpose of this class(and any subclass inheriting it) is to preprocess the data provided by the user and provide utility methods for accessing the data.
class CDSDataLoader():
    def __init__(self):
        raise Exception("This is an interface, please implement it ")
    
    
    def loadData(self): 
        raise Exception("This is an interface method, please implement it ")
     
    #Get all section that we need to parse into sparse matrix
    def getAllSections(self) -> List[str] :
        raise Exception("This is an interface method, please implement it ")
    
    def getQuestionsAnswerForSection(self, sectionName) -> QuestionAnswer :
       raise Exception("This is an interface method, please implement it ")
    
    