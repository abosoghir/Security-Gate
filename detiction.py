import firebase_admin
from firebase_admin import credentials, db
import cv2
import mediapipe as mp
import math


cred = credentials.Certificate(r"D:\_field_training\fir-basic-e2df0-firebase-adminsdk-bejoq-4094500c61.json")  # Replace with your Firebase JSON credentials
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fir-basic-e2df0-default-rtdb.firebaseio.com/'  # Replace with your Firebase database URL
})

# Reference to the Firebase database
gate_state_ref = db.reference('gate_state')

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)

mp_draw = mp.solutions.drawing_utils
mp_hands= mp.solutions.hands 
hands= mp_hands.Hands(max_num_hands=1)

while True:
    success, frame = cap.read()
    if success:
       RGB_frame= cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
       res = hands.process(RGB_frame) 
       if res.multi_hand_landmarks:
           index = res.multi_hand_landmarks[0].landmark[4]
           thumb = res.multi_hand_landmarks[0].landmark[20]
           mp_draw.draw_landmarks(frame,res.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)
           index_x=index.x
           index_y=index.y
           thumb_x=thumb.x
           thumb_y=thumb.y
           distance=math.sqrt((index_x-thumb_x)**2 + (index_y-thumb_y)**2)*10
           print(distance)
           
           cv2.line(frame , pt1=(int(index_x * frame.shape[1]) , int(index_y * frame.shape[0])) , pt2=(int(thumb_x * frame.shape[1]) , int(thumb_y * frame.shape[0])) , color=(255,0,0), thickness=3)
           
           # Send data to Firebase if distance equals 4
           if round(int(distance)) == 4:
                gate_state_ref.set('LASER ON')
           if round(int(distance)) == 0:
                gate_state_ref.set('LASER OFF')    
           
       cv2.imshow("my window",frame)
       if cv2.waitKey(1) == ord("q"):
           break
    
cv2.destroyAllWindows()    
