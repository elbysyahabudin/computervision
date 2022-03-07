import pyfirmata
import time
import cv2

import handTrackingModule as htm
import math

#Arduino's port is connected to COM5. Take a look at Arduino IDE to see which port is connected 
board = pyfirmata.Arduino('COM5')

#LED's pins connected to Arduino
leds = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(detectionCon=0.7)

while True:

    succes, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
        cv2.circle(img, (cx, cy), 15, (0, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)

        if length > 200:
            for leds in range(2, 13):
                board.digital[leds].write(1)
                time.sleep(0.02)
            leds += 1
        elif length < 70:
            for leds in reversed(range(2,13)):
                board.digital[leds].write(0)
                time.sleep(0.02)
            leds +=1

    cv2.imshow('OUTPUT', img)
    cv2.waitKey(1)

