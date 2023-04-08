def getStartAndEndYearFromDataName(dataName):
    dataNameToken = dataName.split("_")
    startYear = ""
    endYear = ""
    if len(dataNameToken) >= 3:
        startYear = dataNameToken[1]
        endYear = dataNameToken[2]

    return (startYear, endYear)