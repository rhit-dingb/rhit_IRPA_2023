
import requests
#Im using request url to make request https://requests.readthedocs.io/en/latest/user/quickstart/
class RasaCommunicator():
    def __init__(self):
        #Connection string to Rasa Server, right now I'm assuming its localhost.
        # "http://137.112.208.157:5005/webhooks/rest/webhook"
        self.connectionString = "http://localhost:5005/"
        
    
    def parseMessage(self,message):
        body = {
        "text": message,
        "message_id": "1"
        }
        #post('https://httpbin.org/post', data={'key': 'value'})
        r = requests.post(self.connectionString+"model/"+"parse", json=body)
        print(r.json())
        return r.json()
        
            


# def main():
#     comm = RasaCommunicator()
#     result = comm.parseMessage("How important is extracurricular-activities in admission decision? ")
#     print(result)

# if __name__ == "__main__":
#     main()
        
    
    
    