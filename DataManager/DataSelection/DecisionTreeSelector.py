
import Data_Ingestion.constants as constants
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
# from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.utils import shuffle
from sklearn.feature_extraction.text import TfidfVectorizer

## EXPERIMENTAL CLASS 
class DecisionTreeSelector():
    def __init__(self):
        pass



    def selectBest(self, questionEntities, sparseMatrices):
        labels = []
        features =[]
        vectorizer = CountVectorizer()
        vectorizer = TfidfVectorizer()

        def f(e):
            return not self.isMetadata(e)
        # vectorizer.fit(X)
        columnsForEachSparse = []
        for sparseMatrix in sparseMatrices:
            columns = sparseMatrix.getColumn()
            columns = list(filter(f, columns ))
            # print(columns)
            columnsForEachSparse.append(" ".join(columns))
        
        # allColumnString = " ".join(list(set(columnsForEachSparse)))
        # print(allColumnString)
        # print(columnsForEachSparse)
        # print(type(columnsForEachSparse))
        vectorizer.fit_transform(columnsForEachSparse)
        print(vectorizer.vocabulary_)
        # print(bow.shape)
        # print(bow.toarray())

        index = 1

        allDocForSparseMatrix = []
        for sparseMatrix in sparseMatrices:
            # print(sparseMatrix.subSectionName)
            for row in sparseMatrix:
              
                rowSparse = []
                for column in row.index:
                    if row[column] and not self.isMetadata(column) == 1:
                        rowSparse.append(column)
                
                if len(rowSparse) == 0:
                    continue


                rowSparse = list(set(rowSparse))
                labels.append(index)
                # print("ROW SPARSE")
                # print(rowSparse)
                # print("LABEL")
                # print(index)
                allDocForSparseMatrix.append(" ".join(rowSparse))

       
            index = index+1

        # print("DEBUG")
        # print(allDocForSparseMatrix)
        transformedVec = vectorizer.transform(allDocForSparseMatrix)
        # print(transformedVec.toarray())
        #model = tree.DecisionTreeClassifier()
        model = RandomForestClassifier( random_state=0)

        X = transformedVec.toarray()
        Y = labels
        X, Y = shuffle(X, Y, random_state=0)

        # model = LogisticRegression(random_state=0)
        model = model.fit(X,Y)
        # print(model.score(X,Y))
        queryVec = vectorizer.transform([" ".join(questionEntities)])
        print(queryVec.toarray())
        res = model.predict(queryVec.toarray())
        
        print("PREDICTION")
        print(res)
        # print(sparseMatrices)
        print(sparseMatrices[res[0]-1].subSectionName)
      

    # PUT HERE FIRST
    def isMetadata(self, value):
        if value.lower() == constants.OPERATION_ALLOWED_COLUMN_VALUE:
            return True
        if value.lower() == constants.SUM_ALLOWED_COLUMN_VALUE:
            return True
        
        if value.lower() == constants.RANGE_ALLOWED_COLUMN_VALUE:
            return True
            
        if value.lower() == constants.PERCENTAGE_ALLOWED_COLUMN_VALUE:
            return True
        
        if value.lower() == constants.DENOMINATOR_QUESTION_COLUMN_VALUE:
            return True

        if value.lower() == "value":
            return True

        if value.lower() == "template":
            return True

        if value.lower() == "about":
            return True

        return False
                    

