from enum import Enum, auto
class EventType(Enum):
    ModelChange = 1
    DataUploaded = 2
    DataDeletion = 3