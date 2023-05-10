
import json
import requests
import asyncio
import aiohttp
#Im using request url to make request https://requests.readthedocs.io/en/latest/user/quickstart/
class RasaCommunicator():
    """
    Class used to communicate with Rasa to run certain actions in the action certain.
    """
    def __init__(self):
        #Connection string to Rasa Server, right now I'm assuming its localhost.
        # "http://137.112.208.157:5005/webhooks/rest/webhook"
        self.connectionString = "http://localhost:5005/"
        
    
    async def parseMessage(self,message, session):
        body = {
        "text": message,
        "message_id": "1"
        }

        body = json.dumps(body)
        async with session.post(self.connectionString+"model/"+"parse", headers ={ "Content-Type": "application/json" }, data = body) as response:
                return await response.json()
                


    async def parseMessagesAsync(self, messages):
        tasks = []
        async with aiohttp.ClientSession() as session:
            for message in messages:
                task = asyncio.create_task(self.parseMessage(message, session=session))
                tasks.append(task)

            responses = await asyncio.gather(*tasks)
            return responses


        
    # http://localhost:5005/conversations/{conversation_id}/trigger_intent
    async def injectIntent(self, intent, entities, session, convId):
        """
        This function will inject an intent to rasa which will trigger an action we specified in the stories.yml
        that the Rasa model was trained on. 
        """
        print("USING INTENT")
        print(intent)
        body={
            "name": intent,
            "entities": entities
        }

        body = json.dumps(body)
        async with session.post(self.connectionString+"conversations/"+convId+"/trigger_intent",
        headers ={ "Content-Type": "application/json" }, data = body) as response:
            return await response.json()

    