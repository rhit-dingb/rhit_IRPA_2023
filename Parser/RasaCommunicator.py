
import json
import requests
import asyncio
import aiohttp
#Im using request url to make request https://requests.readthedocs.io/en/latest/user/quickstart/
class RasaCommunicator():
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

  


        # print(body)
        # #post('https://httpbin.org/post', data={'key': 'value'})
        # r = requests.post(self.connectionString+"model/"+"parse", json=body)
        # return r.json()
        
    # http://localhost:5005/conversations/{conversation_id}/trigger_intent
    async def injectIntent(self, intent, entities, session, convId):
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

# def main():
#     comm = RasaCommunicator()
#     result = comm.parseMessage("How important is extracurricular-activities in admission decision? ")
#     print(result)

# if __name__ == "__main__":
#     main()
        
    
    
    