import cv2
import numpy as np
import mediapipe as mp
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def findPosition(img, handNo=0, draw=True):
    lmList = []
    if results.multi_hand_landmarks:
        myHand = results.multi_hand_landmarks[handNo]
        for id, lm in enumerate(myHand.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)

            lmList.append([id,cx,cy])

    return lmList

def findHands(img,draw=True):
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            if draw:
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
    return img


mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils


cap = cv2.VideoCapture(0)



devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = (volume.GetVolumeRange())

minVol = volRange[0]
maxVol = volRange[1]



while True:
    success, img = cap.read()

    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)  # sending rgb image to hands object so we have to first convert it which is this line because hands object only takes rgb image

    results = hands.process(imgRGB)

    findHands(img)
    lmList = findPosition(img)
    if len(lmList) != 0:

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1, y1), 15, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)

        length = math.hypot(x2-x1, y2-y1)

        vol = np.interp(length, [50, 240], [minVol, maxVol])
        volume.SetMasterVolumeLevel(vol, None)


        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0, 0, 255), cv2.FILLED)


    cv2.imshow("image", img)
    cv2.waitKey(1)
