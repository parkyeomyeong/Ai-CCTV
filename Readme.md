Ai-CCTV(iot security system)
--------
> 1. 개요
- 요즘 코로나 시대로 택배로 물건을 받는 경우가 많은데 누군가 집 현관에 택배를 가져가는 경우에 대처할 방법이 없었습니다. 그래서 집앞에 누군가 나타났을때 누구인지 인식을하고 등록된 사람(가족들)이 아닌경우 안드로이드 앱 으로 알림이 오게되어 실시간으로 현관을 모니터링하고 수상한 사람이 집 앞에 있다면 경고음을 내서 쫒아내고자 Ai-CCTV를 만들 생각을 했습니다.

- **사용 H/W, 라이브러리**

      - H/W : raspberry pi, Web cam, Buzzer
      - library : Flask, Face_recognition etc...
      - Cloud Server: AWS
      
> 2. 기능
- **Raspberry Pi**
            
      - Real time image(using Flask)
      - Data publishing(Person, Time imformation to aws)
      - Data Reciveing(for Buzzer control) 
      
- **Android App**

      - Log inquiry
      - Buzzer control
      - Monitoring

> 3. 기능구현

- Project architecture

![123](https://user-images.githubusercontent.com/68410186/101429729-f8d2f180-3946-11eb-9123-bfa221512081.png)

- **IoT 백엔드**는 AWS의 다양한 서비스(AWS IoT Core, AWS Lambda, Amazon DyanmoDB, Amazon SNS, Amazon API Gateway)를 이용해 구축된 IoT 클라우드 플랫폼입니다.
  - **AWS IoT Device gateway**를 통해서 연결된 디바이스(Raspberry)로부터 디바이스 정보(사람, 감지했을때 시간)를 수신하고, **MQTT 프로토콜**을 이용하여 **Device shadow** 혹은 **IoT rule** 컴포넌트와 상호작용합니다.
    - **Device shadow**는 **Device gateway**를 통해 게시된 주제에 따라 디바이스 상태정보를 업데이트하거나 현재 상태정보를 게시합니다.
    - **IoT rule**은 등록된 주제(update/accepted)의 메시지가 수신될 때마다 **AWS Lambda** 함수를 통해서 수신된 메시지를 **Amazon DynamoDB**에 저장합니다.
  
- **Raspberry Pi**
  - main.py 에 falsk 모듈 사용 gen에서 while loop을 돌며 webcamvideostream.py 로 계속해서 영상을 찍음
  - 찍은 **Frame**을 detectFace.py에 **detect함수**의 parameter로 줘서 등록된 사진과 있는지 찾아내며 그 영상을 송출합니다.
  - 만약 **Frame**에 등록된 사람이 있다면 **awsiotConnection.py**의 **publisingMessage함수**에 해당 라즈베리파이 이름, 찾아낸 사람 parameter로 전달(등록된 사람이 아니라면 Unknown 을 name parameter로)
  - **publishingMessage**는 aws iot core와 MQTT통신하는 SDK를 사용한 메소드이며 인자로는 (TOPIC, json, 0) 형식으로 건넨다
    - TOPIC
      
            $aws/things/Your device name/shadow/update
      
    - json
    
            { "state" : { "reported": { "device": Device, "time": Time, "Person": Person #,"Buzzer": self.temp }}}
            
  - TOPIC으로 json을 보내면 위 그림처럼 Device gateway에 device/shadow/update/accepted로 message가 오면 이 TOPIC을 구독한 Iot rule이 그 Massage를 등록된 Lambda에 event parameter로 넘겨줍니다.
  - aws 만들어 놓은 Lambda function은 dynamoDB에 Data를 저장합니다.
  
- **Android App**
  - Raspberry Pi에 송출한 영상의 url주소를 WebView로 load 합니다.
  - **REST API** 설계
    - 디바이스 상태 변경(Sound ON, Sound OFF 버튼 누를 때 Buzzer 제어)
    
            PUT /devices/{deviceId}
            
      - message body (payload)
      
                  { "tags" : [ { "attrName": "Buzzer", "attrValue": "ON"}]}
                  
      - 디바이스 로그 조회(상단 View버튼 클릭시 나오는 Activity에 날짜 설정 후 조회버튼 누를 때)
      
                  GET /devices/{deviceId}/log?from=yyyy-mm-dd hh:mm:ss&to=yyyy-mm-dd hh:mm:ss
  - 상태 변경 AIP URI(Buzzer control)
  
            https://xxxxxxxx.execute-api.ap-northeast-2.amazonaws.com/prod/devices/{devices_name}
            
  - 로그 조회 API URI
  
            https://xxxxxxxx.execute-api.ap-northeast-2.amazonaws.com/prod/devices/{devices_name}/log
            
