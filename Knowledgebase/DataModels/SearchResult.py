class SearchResult():
    def __init__(self, answer,entitiesUsed, type, realQuestion):
        # print("CHANGE ANSWER")
        # print(answer)
        self.answer = answer
        self.entitiesUsed = entitiesUsed
        self.type = type
        self.question = realQuestion

    
    def changeAnswer(self,answer):
      
        self.answer = answer


