import cv2
import numpy as np
import mediapipe as mp 
import tensorflow as tf
from tensorflow.keras.models import load_model


mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence = 0.7)
mpDraw = mp.solutions.drawing_utils

#tensorflow
model=load_model('mp_hand_gesture')

#class
f = open('gesture.names','r')
classNames = f.read().split('\n')
f.close()
print(classNames)

#webcam  
cap = cv2.VideoCapture(0)

while True:
    #reading each frame 
    _, frame = cap.read()
    
    x, y, c = frame.shape
    
    #flip the frame vertically
    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    #HANDLANDMARK PREDICTION
    result = hands.process(framergb)
    
    className = ''
    
    #before result 
    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                # print(id, lm)
                lmx = int(lm.x * x)
                lmy = int(lm.y * y)
                
                landmarks.append([lmx, lmy])
                
                
            #drawing landmarks on frames
            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)
            
            #predict gesture
            prediction = model.predict([landmarks])
            #print(prediction)
            classID = np.argmax(prediction)
            className = classNames[classID]
            
    #show the prediction on the frame
    cv2.putText(frame, className, (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,225), 2, cv2.LINE_AA)
    #finaloutput
    cv2.imshow("Output", frame)
    
    if cv2.waitKey(1) == ord('q'):
        break
#release the webcam and destroy al active windows

cap.release()

cv2.destroyAllWindows()
            
            
                

