
from Knowledgebase.DefaultShouldAddRow import DefaultShouldAddRowStrategy
from Knowledgebase.ShouldAddRowStrategy import ShouldAddRowStrategy
"""
Strategy for choosing which appropriate specific column of CDS table we will use, based on entities extracted from user input.
This is mainly used when a column in a cds table is includes value from previous column. For example,this happens 
for  the enrollment by race table on CDS file. We want to choose a specific column to use to avoid summing up values for both columns
 
choices: list of choices that look something like this: 
[
    {
            "columns": ["degree-seeking", "first-time", "first-year"]
    }, 
    {
            "columns": ["degree-seeking", "non-first-time", "non-first-year"],
            "isDefault":True
    }
]

Each choice is an object describing the entities that applies to the specific column of the table in quetion on cds. 
This example is for the enrollment by race table on cds. The first column for that table says:
"Degree-seeking, First-time First year" and the second column says "Degree-seeking, Undergraduates (include first-time first-year)"

If we represent it in sparse matrix, these two rows will have almost no difference and the values under the columns mentioned above will
will be summed up together. To prevent this:

1. I edited set first-time, first-year to 0 in the excel sheet for numbers that were under the column of the CDS table for enrollment by race: 
"Degree-seeking, First-time First year". 

Because, although first-time and first-year are implied to be true for this column since it include that information, but if 
the user inputs "What is first-time and first-year hispanic students enrolled?", we would only like to only the value for the first 
column. We want to avoid summing those two column up.

2. The determineShouldAddRow function will first iterate through the extracted entities and see which choice has the most number
of matching entities, and use the number for that choice by returning true and will return false for all other.
--this would be the case when use ask for specifics like first-time, first-year.

If there is a tie between match -- this would be the the case when the user asked "how many asian students are enrolled?"
Then, we would default to the column choice that has isDefault set to true, which is the second column of the enrollment by race table,
which would give the user the total Degree-seeking Undergraduates who are asian students.


3. The entities/columns specified for the second choice has non-freshman and non-first year because currently, there is no way to
distinguish between values that belongs to the first column of enrollment by race table from the second column. Since we want to 
route questions about non-freshman and non-first-year to this column, I took advantage of that to create distinction between the two 
choices.

"""
class ChooseFromOptionsAddRowStrategy(ShouldAddRowStrategy):
    
    def __init__(self,  choices):
        super().__init__()
        self.choices = choices
        self.defaultShouldAddRow = DefaultShouldAddRowStrategy()
    
    def determineShouldAddRow(self, row, entities, sparseMatrix):
        maxMatches = [] 
        matchCount = 0
        currMax = 0
        for choice in self.choices:
            matchCount = 0
            for entityExtracted in entities:
                if entityExtracted in choice["columns"]:
                    matchCount = matchCount + 1

            if matchCount > currMax:
                maxMatches = []
                maxMatches.append(choice)
                currMax = matchCount
            
            elif matchCount == currMax:
                maxMatches.append(choice)
                
        if len(maxMatches) == 1:
            
            entitiesUsedToMatch =  self.defaultShouldAddRow.determineShouldAddRow(row, list(set(maxMatches[0]["columns"]+entities)), sparseMatrix )
            return self.getEntityUsed(entitiesUsedToMatch, entities)
        else:
            for choice in self.choices:
                if "isDefault" in choice and choice["isDefault"]:
                    entitiesUsedToMatch  = self.defaultShouldAddRow.determineShouldAddRow(row, list(set(choice["columns"]+entities)), sparseMatrix )
                   
                    return self.getEntityUsed(entitiesUsedToMatch,entities)

        
    def getEntityUsed(self,entitiesUsedToMatch, extractedEntities):
        entitiesActuallyUsed = []
        for entity in entitiesUsedToMatch: 
            if not entity in extractedEntities:
                continue
            else: 
                entitiesActuallyUsed.append(entity)

        return entitiesActuallyUsed
                