from typing import Tuple

from Knowledgebase.SearchResultType import SearchResultType

class TypeController():
    def determineResultType(self, searchResult) -> Tuple[any, SearchResultType]:
            try:
                searchResult = int(searchResult)
                return (searchResult, SearchResultType.NUMBER)
            except ValueError:
                if searchResult.replace(".", "", 1).isdigit():
                    return (float(searchResult), SearchResultType.FLOAT)
                #Otherwise the value is string if it is not integer or float.
                else:
                    if "%" == searchResult[len(searchResult)-1]:
                        return (searchResult, SearchResultType.PERCENTAGE)
                    else:
                        return (searchResult, SearchResultType.STRING)
