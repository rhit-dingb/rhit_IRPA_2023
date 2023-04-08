


from typing import Dict, List

from CacheLayer.EventSubscriber import EventSubscriber
from CacheLayer.EventType import EventType
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import asyncio

class CacheEventPublisher():
    def __init__(self):
    #    print(os.listdir("../models/"))
        self.DIRECTORY_TO_WATCH = "../models/" 
        self.subscribers : List[EventSubscriber] = []
       
    async def startObserver(self):
        self.observer = Observer()
        event_handler = FileSystemEventHandler()
        event_handler.on_any_event = self.changeInDirectory
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        print("DONE")
        self.observer.join()


    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def changeInDirectory(self, event):
        print(event)
        # 
        asyncio.run(self.notify(EventType.ModelChange, dict())) 

    async def notify(self, eventType : EventType, eventData : Dict[str, any]):
        for subscriber in self.subscribers:

            if subscriber.isEventType(eventType):
               await subscriber.notify(eventData)
