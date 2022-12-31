from typing import Tuple

from Knowledgebase.SearchResultType import SearchResultType

class TypeController():
    def determineResultType(self, searchResult) -> Tuple[any, SearchResultType]:
            if searchResult == None:
                return (searchResult, None)
            try:
                searchResult = int(searchResult)
                return (searchResult, SearchResultType.NUMBER)
            except Exception:
                searchResult = str(searchResult)
                if searchResult.replace(".", "", 1).isdigit():
                    return (float(searchResult), SearchResultType.FLOAT)
                #Otherwise the value is string if it is not integer or float.
                else:
                    if len(searchResult) > 0 and "%" == searchResult[-1]:
                        # print("CASTED SEARCH RESULT")
                        # print(searchResult)
                        return (searchResult, SearchResultType.PERCENTAGE)
                    else:
                        return (searchResult, SearchResultType.STRING)
