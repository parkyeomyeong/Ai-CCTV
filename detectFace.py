import cv2
import face_recognition #I used this module to create a face-finding file.-yeomyeong
import numpy as np
import time
from awsiotConnection import awscommunication

yeo_image = face_recognition.load_image_file("images\\yeo.jpg")
yeo_face_encoding = face_recognition.face_encodings(yeo_image)[0]

sun_image = face_recognition.load_image_file("images\\sunjae.jpg")
sun_face_encoding = face_recognition.face_encodings(sun_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    yeo_face_encoding,
    sun_face_encoding
]
known_face_names = [
    "yeomyeong",
    "sunjae"
]

class face_detecting:
    def __init__(self):
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True
        
        self.lasttime = time.time()# Set the variable to avoid calling lambda every moment Because we continue to detect face, taking pictures in a row
        self.lastname = ""#set the variaable the same reason

    def detect(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if self.process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            self.face_locations = face_recognition.face_locations(rgb_small_frame)
            self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

            self.face_names = []
            for face_encoding in self.face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                if time.time() - self.lasttime > 5 and name != self.lastname :
                    self.lasttime = time.time()
                    self.lastname = name
                    awscommunication().publisingMessage("raspberry",name)#publishing to aws-iot-core(iot-Shadow)
                

                self.face_names.append(name)

        self.process_this_frame = not self.process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        
        return frame
