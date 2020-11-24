# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient # SDK for mqtt communication
import json
import time

class awscommunication :
    def __init__(self):
        # certificate information for aws-iot-core access
        self.ENDPOINT = "your endpoint"
        self.CLIENT_ID = "cctvDevice"
        self.PATH_TO_CERT = "certificates\\your-certificate.pem.crt"
        self.PATH_TO_KEY = "certificates\\your-private.pem.key"
        self.PATH_TO_ROOT = "certificates\\root.pem"
        self.TOPIC = "you topic"#this topic is used by aws-Lambda to Store the message in dynamoDB  

    def publisingMessage(self, Device, Person) :

        #The face is recognized when this method is executed. Therefore, save time when it is recognized
        Time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
        #making json type
        str = {
            "state" : {
                "reported": {
                    "device": Device,
                    "time": Time,
                    "Person": Person
                    }
                }
        }
        # string to json
        jsonstr = json.dumps(str)

        #this section is aws-SDK example
        myMQTTClient = AWSIoTMQTTClient("myClientID")
        myMQTTClient.configureEndpoint(self.ENDPOINT, 8883)
        myMQTTClient.configureCredentials(self.PATH_TO_ROOT, self.PATH_TO_KEY, self.PATH_TO_CERT)
        myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
        myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

        myMQTTClient.connect()
        myMQTTClient.publish(self.TOPIC, jsonstr, 0)#publish the json that created so that they can be used by Lambda.
        myMQTTClient.disconnect()
