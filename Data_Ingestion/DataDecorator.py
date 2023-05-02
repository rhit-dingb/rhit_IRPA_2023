
from Data_Ingestion.DataProcessor import DataProcessor

class DataDecorator(DataProcessor):
    """
    The base Decorator class follows the same interface as the other components.
    The primary purpose of this class is to define the wrapping interface for
    all concrete decorators. The default implementation of the wrapping code
    might include a field for storing a wrapped component and the means to
    initialize it.
    """

    dataProcessor : DataProcessor

    def __init__(self, decorated : DataProcessor) -> None:
        self.decorated = decorated

    
    def getDataByDbNameAndSection(self, client,section : str, dbName : str):
        return self.decorated.getDataByDbNameAndSection(client, section, dbName)


