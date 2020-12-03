# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient # SDK for mqtt communication
from buzzer import buzzer_control # for rasspberry buzzer control method
import json
import time
import ast

class awscommunication :
    def __init__(self):
        # certificate information for aws-iot-core access
        self.ENDPOINT = "your endpoint"
        self.CLIENT_ID = "cctvDevice"
        self.PATH_TO_CERT = "certificates\\your certificate"
        self.PATH_TO_KEY = "certificates\\your private key"
        self.PATH_TO_ROOT = "certificates\\you root"
        self.PUB_TOPIC = "$aws/things/Your device name/shadow/update"#this topic is used by aws-Lambda to Store the message in dynamoDB  
        self.SUB_TOPIC = "$aws/things/Your device name/shadow/update/delta"#Receive buzzer control message from app
        self.temp=""
        #this section is aws-SDK example
        self.myMQTTClient = AWSIoTMQTTClient("myClientID")
        self.myMQTTClient.configureEndpoint(self.ENDPOINT, 8883)
        self.myMQTTClient.configureCredentials(self.PATH_TO_ROOT, self.PATH_TO_KEY, self.PATH_TO_CERT)
        self.myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
        self.myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

        self.myMQTTClient.connect()

    #This is uesed by subscribeMessage method. Execute when a message is received from a subscription to receive a buzzer control message.
    def customCallback(self, client, userdata, message):
        self.answer = message.payload.decode('utf-8')#HTTP respones resource is Byte Stream, so type is 'bytes '
        dic = ast.literal_eval(self.answer)
        self.temp = dic['state']['Buzzer']
        if self.temp == "ON":
            buzzer_control("ON")
        elif self.temp == "OFF":
            buzzer_control("OFF")
        
        #self.myMQTTClient.disconnect()
        

    def publisingMessage(self, Device, Person) :

        #The face is recognized when this method is executed. Therefore, save time when it is recognized
        Time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        #making json type
        str = {
            "state" : {
                "reported": {
                    "device": Device,
                    "time": Time,
                    "Person": Person
                    #,"Buzzer": self.temp
                    }
                }
        }
        # string to json
        jsonstr = json.dumps(str)

        self.myMQTTClient.publish(self.PUB_TOPIC, jsonstr, 0)#publish the json that created so that they can be used by Lambda.
        #self.myMQTTClient.disconnect()

    def subscribeMessage(self):
        self.myMQTTClient.subscribe(self.SUB_TOPIC,1,self.customCallback)
        #time.sleep(10)
        #myMQTTClient.disconnect()
