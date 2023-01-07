from typing import Tuple

from Knowledgebase.SearchResultType import SearchResultType

class TypeController():
    def determineResultType(self, searchResult) -> Tuple[any, SearchResultType]:
            if searchResult == None:
                return (searchResult, None)
            if len(searchResult) == 0:
                return (searchResult, SearchResultType.STRING)
            try:
                searchResult = int(searchResult)
                return (searchResult, SearchResultType.NUMBER)
            except Exception:
                searchResult = str(searchResult)
                if searchResult.replace(".", "", 1).isdigit():
                    return (float(searchResult), SearchResultType.FLOAT)
                #Otherwise the value is string if it is not integer or float.
                elif "%" == searchResult[-1]:
                    # print("CASTED SEARCH RESULT")
                    # print(searchResult)
                    val = self.tryCastToFloat(searchResult[1:])
                    if val is None:
                        return (searchResult, SearchResultType.STRING)
                    return (val, SearchResultType.PERCENTAGE)
                elif searchResult[0] == "$":
                    val = self.tryCastToFloat(searchResult[1:])
                    if val is None:
                        return (searchResult, SearchResultType.STRING)
                    return (val, SearchResultType.DOLLAR)
                else:
                    return (searchResult, SearchResultType.STRING)

    def tryCastToFloat(self, value):
        try:
            floatVal = float(value)
            return floatVal
        except Exception:
            return None

