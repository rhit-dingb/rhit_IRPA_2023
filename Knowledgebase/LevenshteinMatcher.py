from Knowledgebase.Matcher import Matcher
import numpy as np

class LevenshteinMatcher(Matcher):
    # threshold is the max number of difference in characters that should be allowed.
    # so if the closest match strings have a difference greater than threshold, an empty list will be returned.
    def __init__(self, threshold):
        self.threshold = threshold

    
    def match(self, keys, entities) -> tuple:
        similarities = []
        for entity in entities:
            for key in keys:
                entityNoSpace = entity.lower().replace(" ", "")
                keyNoSpace = key.lower().replace(" ", "")
                editLength = self.levenshtein(entityNoSpace, keyNoSpace)
                similarities.append((entity, key, editLength))
        
        
        minSim = self.findMin(similarities)
        if minSim[2] > self.threshold:
            return ()
        else:
            return minSim

    def findMin(self, similarities):
        min = None
        minPair = None
        for sim in similarities:
            if min is None or sim[2]<min:
                min = sim[2]
                minPair = sim
        
        return minPair

    # function to calculate number of edits required between two strings for them to be the same
    # code taken from https://stackabuse.com/levenshtein-distance-and-text-similarity-in-python/

    def levenshtein(self, seq1, seq2):
        size_x = len(seq1) + 1
        size_y = len(seq2) + 1
        matrix = np.zeros ((size_x, size_y))
        for x in range(size_x):
            matrix [x, 0] = x
        for y in range(size_y):
            matrix [0, y] = y

        for x in range(1, size_x):
            for y in range(1, size_y):
                if seq1[x-1] == seq2[y-1]:
                    matrix [x,y] = min(
                        matrix[x-1, y] + 1,
                        matrix[x-1, y-1],
                        matrix[x, y-1] + 1
                    )
                else:
                    matrix [x,y] = min(
                        matrix[x-1,y] + 1,
                        matrix[x-1,y-1] + 1,
                        matrix[x,y-1] + 1
                    )
        #print (matrix)
        return (matrix[size_x - 1, size_y - 1])