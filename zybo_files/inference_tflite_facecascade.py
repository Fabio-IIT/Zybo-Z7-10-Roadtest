import tensorflow as tf
import cv2
from keras.models import load_model
import numpy as np

import json
import select
import v4l2capture
import time

from pwm_rgb import PWM_RGB,BLUE,GREEN,RED

pwm=PWM_RGB(4,0)
pwm.setPeriod(60000)
pwm.red()
pwm.enable()

modelfile='./model_full_face_recognition.h5'

allowed = None

with open("allowed.json", "r") as read_file:
    allowed = json.load(read_file)

try:
    import cPickle as pickle
except ImportError:  # python 3.x
    import pickle

with open('labels.p', 'rb') as fp:
    label_map = pickle.load(fp)

# Load TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(model_path="converted_model.tflite")
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Open the video device.
video = v4l2capture.Video_device("/dev/video0")
size_x, size_y = video.set_format(1920, 1080)
video.create_buffers(1)
video.queue_all_buffers()

# Start the device.
video.start()
time.sleep(10)

while True:
    # Wait for the device to fill the buffer.
    select.select((video,), (), ())
    image_data = video.read_and_queue()
    frame_mat = np.reshape(np.frombuffer(image_data, dtype=np.uint8),(size_y,size_x,3),order='C')
    frame_mat=cv2.flip(frame_mat, 0)

    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
    gray_mat = cv2.cvtColor(frame_mat, cv2.COLOR_BGR2GRAY)
    start_time=time.time()    
    faces = faceCascade.detectMultiScale(
        gray_mat,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(50, 50),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    print("Detection run time: %s s" % (time.time()-start_time))
    if len(faces)==0:
        print("no faces detected")
        pwm.red()
        continue
   
    pwm.blue()

    (x,y,w,h)=faces[0] 
    frame_mat = frame_mat[y:y + h, x:x + w]
    frame_mat=cv2.resize(frame_mat,(150,150))
    frame_mat=np.reshape(frame_mat,[1,150,150,3])

    input_data = frame_mat.astype('float32')

    interpreter.set_tensor(input_details[0]['index'], input_data)

    try:
        start_time=time.time()
        interpreter.invoke()
        print("Recognition run time: %s s" % (time.time()-start_time))
    except:
        raise Exception("invoke failed!")

    output_data = interpreter.get_tensor(output_details[0]['index'])
    id = [key  for (key, value) in label_map.items() if value == np.argmax(output_data)][0]
    if id in allowed.keys():
        pwm.green()
        print("User \033[1;32m%s : ACCESS GRANTED!\033[0;30m" % allowed[id])
    else:
        pwm.red()
        print("User \033[1;31munrecognized : ACCESS DENIED!\033[0;30m")
            
    time.sleep(5)

video.close()
