import cv2
import sys
import threading
from flask import Flask, render_template, Response
from webcamvideostream import WebcamVideoStream
from flask_basicauth import BasicAuth
from detectFace import face_detecting


# App Globals (do not edit)
app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = ''
app.config['BASIC_AUTH_PASSWORD'] = ''
app.config['BASIC_AUTH_FORCE'] = False

basic_auth = BasicAuth(app)
last_epoch = 0

@app.route('/')
@basic_auth.required
def index():
    return render_template('index.html')

def gen(camera):

    model = face_detecting()#Bring the object in detectFace.py

    while True:
        if camera.stopped:
            break

        frame = camera.read()#Bring the frame from the camera(Webcam)
        frame = model.detect(frame)#

        ret, jpeg = cv2.imencode('.jpg',frame)
        if jpeg is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
        else:
            print("frame is none")

@app.route('/video_feed')
def video_feed():
    return Response(gen(WebcamVideoStream().start()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
