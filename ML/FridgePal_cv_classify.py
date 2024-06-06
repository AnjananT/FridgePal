import cv2
import tensorflow as tf
from keras.preprocessing import image
from keras.preprocessing.image import img_to_array
import numpy as np
import requests
import serial


model = tf.keras.models.load_model("fine_tuned_model2.keras")
url = 'http://localhost:5000/update_labels'
#ser = serial.Serial('COM7', 115200, timeout=1)

def preprocess_image(img):
    img = cv2.resize(img, (100, 100))
    img = img.astype("float") / 255.0
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    return img

def classify_image(img):
    img = preprocess_image(img)
    pred = model.predict(img)
    return pred

def display_result(frame, pred):
    class_names = ['bread', 'lettuce', 'mayonnaise', 'tomato']
    max_prob_idx = np.argmax(pred)
    class_label = class_names[max_prob_idx]
    confidence = pred[0][max_prob_idx]
    cv2.putText(frame, f"{class_label}: {confidence:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    payload = {'class': class_label}
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print('Stats updated successfully')
    else:
        print('Failed to update stats')

    print(f'The predicted class is {class_label}')
    
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow('frame', frame)

    #arduino_data = ser.readline().decode().strip()
    key = cv2.waitKey(1)
    if key==ord('j'):
        pred = classify_image(frame)
        display_result(frame, pred)
        cv2.imshow('frame', frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    elif key == ord('q'):  # Press 'q' to exit
        break

cap.release()
cv2.destroyAllWindows()