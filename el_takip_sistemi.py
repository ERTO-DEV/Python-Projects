import cv2
import mediapipe as mp
import os

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

def count_fingers(hand_landmarks):
    fingers = []
    tip_ids = [4, 8, 12, 16, 20]

    if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0] - 2].x:  
        fingers.append(0)
    else:
        fingers.append(1)

    for i in range(1, 5):
        if hand_landmarks.landmark[tip_ids[i]].y < hand_landmarks.landmark[tip_ids[i] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                fingers = count_fingers(hand_landmarks)
                total_fingers = fingers.count(1)
                debug_output = [1 if i < total_fingers else 0 for i in range(5)]

                print(f"Parmak Sayısı: {total_fingers}, Debug: {debug_output}")

                if total_fingers == 1:
                    os.system("start https://www.google.com")
                
                #if total_fingers == 2:
                 #   os.system("taskkill /F /IM explorer.exe & start explorer.exe")

                if total_fingers == 4:
                   os.system('start "" "D:\\Şarkılar\\Diriliş Ertuğrul Jenerik Earrape (Bass Boosted).mp4"')


                if total_fingers == 0:
                    os.system("shutdown /s /t 1")  

                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow('El takip sistemi, by-erto', image)

        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
