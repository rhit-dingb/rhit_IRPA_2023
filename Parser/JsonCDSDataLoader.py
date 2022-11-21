
from ast import Dict
from typing import List
from Parser.QuestionAnswer import QuestionAnswer
from Parser.CDSDataLoader import CDSDataLoader

basisForSelectionQuestionAnswers = {
    "sections" : ["basis for selection"],
    "basis for selection": { "questions": ["What is the importance of the rigor of secondary school record in admission decisions?",
                                           "What is the importance of class rank in admission decisions?",
                                            "What is the importance of academic gpa in admission decisions?",
                                            "What is the importance of standardized test scores in admission decisions?",
                                            "What is the importance of application essays in admission decisions?",
                                            "What is the importance of recommendation in admission decisions?",
                                            "What is the importance of interviews in admission decisions?",
                                            "What is the importance of extracurricular activities in admission decisions?",
                                            "What is the importance of talent/ability in admission decisions?",
                                            "What is the importance of character/personal qualities in admission decisions?",
                                            "What is the importance of being a first generation student in admission decisions?",
                                            "What is the importance of alumni/ae relation in admission decisions?",
                                            "What is the importance of geographical residence in admission decisions?",
                                            "What is the importance of state residency in admission decisions?",
                                            "What is the importance of religious affiliation/commitment in admission decisions?",
                                            "What is the importance of racial/ethnic status in admission decisions?",
                                            "What is the importance of volunteer work in admission decisions?",
                                            "What is the importance of work experience in admission decisions?",
                                            "What is the importance of level of applicant's interest in admission decisions?",
                                          ],
                                          
                            "answers":["very important",
                                        "considerd",    
                                        "very important",  
                                        "considered",
                                        "considerd",
                                        "important",
                                        "considered",
                                        "important",
                                        "considered",
                                        "considered",
                                        "considered",
                                        "considered",
                                        "considered",
                                        "not considerd",
                                        "not considerd",
                                        "considered",
                                        "considered",
                                        "considered",
                                        "considered"
                                        
                                       ]
    }
}

class JsonCDSDataLoader(CDSDataLoader):
    def __init__(self):
        self.data = basisForSelectionQuestionAnswers
    
    def loadData(self): 
       return
     
    
    #Get all section that "we need to parse into sparse matrix, including sub sections 
    def getAllSections(self) -> List[str] :
        return self.data["sections"]
    

    
    def getQuestionsAnswerForSection(self, sectionName) -> QuestionAnswer :
       res = []
       if sectionName in self.data.keys():
           questionsAndAnswers : Dict = self.data[sectionName]
           questions : List[str] = questionsAndAnswers["questions"]
           print(len(questions))
           answers : List[str] = questionsAndAnswers["answers"]
           print(len(answers))
           for i in range(len(questions)):
               res.append(QuestionAnswer(questions[i], answers[i], []))
           
        #    for questionAns"wer in self.data[sectionName]:
        #         res.append(QuestionAns"wer(questionAns"wer["question"], questionAns"wer["ans"wer"], []))
                
           return res
       else:
           return []
    