
from Data_Ingestion.DataProcessor import DataProcessor

class DataDecorator(DataProcessor):
    """
    The decorator class that will be inherited by the different decorator to convert data into different internal models.
    """

    dataProcessor : DataProcessor

    def __init__(self, decorated : DataProcessor) -> None:
        self.decorated = decorated

    
    def getDataByDbNameAndSection(self, client,section : str, dbName : str):
        return self.decorated.getDataByDbNameAndSection(client, section, dbName)


