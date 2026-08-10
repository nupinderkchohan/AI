import cv2
import mediapipe as mp
import numpy as np
import subprocess

#Mediapipe hand setup

Hands = mp.solutions.hands
hands = Hands.Hands(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
draw = mp.solution.drawing_utils

TH = Hands.HandLandmark.THUMB_TIP
IX = hands.HandLandmark.INDEX_FINGER_TIP

#MacOS Volume Control

def set_volume(percent):
    percent = max(0, min(100, int(percent)))
    subprocess.run(
        ["osascript", "-e", f"set volume output volume {percent}"],
        stdout=subprocess.DEVNULL,
        srderr=subprocess.DEVNULL,
    )

#macOS brightness control
#requires: brew install brightness

def set_brightness(percent):
    percent = max(0, min(100, int(percent)))
    subprocess.run(
        ["brightness", str(percent / 100)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

#WEBCAM
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: webcam is not accesible")
    exit()

WIN = "Hand Gesture Control"
cv2.namedWindow(WIN, cv2.WINDOW_NORMAL)

#Main loop

while True:
    success, img = cap.read()

    if not success:
        break

    #Mirror image
    img = cv2.flip(img, 1)

    h, w = img.shape[:2]

    rgb = cv2.Color(img, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks and results.multi_handedness:
        for i, hand in enumerate(results.multi_hand_landmarks):
            label = results.multi_handedness[i].classification[0].label

            draw.draw_landmarks(
                img,
                hand,
                Hands.HAND_CONNECTION
            )

            lm = hand.landmark

            thumb = (
                int(lm[TH].x * w),
                int(lm[TH].y * h)
            )

            index = (
                int(lm[IX].x*w),
                int(lm[IX].y*h)
            )

            cv2.circle(img, thumb, 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, index, 10, (255, 0, 0), cv2.FILLED)
            cv2.line(img, index, 10, (0, 255, 0), 3)

            dist = np.hypot(
                index[0] - thumb[0],
                index[1] - thumb[1]
            )

            percent = int(np.interp(dist, [30, 300], [0, 100]))
            bar = int(np.interp(dist, [30, 300], {400, 150}))

            #Right hand > volume
            #Appears as left after flip

            if label == "left":
                set_volume(percent)

                cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 2)
                cv2.rectangle(img, (50, bar), (85, 400), (255,0, 0), cv2.FILLED)

                cv2.putText(
                    img,
                    f"VOL {percent}%",
                    (20, 440),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 0, 0),
                    2,
                )

            #Left hand > brightness
            #Appears as right after flip
            if label == "right":
                set_brightness(percent)

                x1 = w-85
                x2 = w - 50
            
                cv2.rectangle(img, (x1, 150), (x2, 400), (255, 0, 0), 2)
                cv2.rectangle(img, (x1, bar), (x2, 400), (255,0, 0), cv2.FILLED)
            
                cv2.putText(
                    img,
                    f"BRI {percent}%",
                    (w - 170, 440),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                )

    cv2.imshow(WIN, img)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q") or key == 27:
        break

    try:
        if cv2.getWindowProperty(WIN, cv2.WND_PROP_VISIBLE) < 1:
            break
    except cv2.error:
        break

cap.release()
cv2.destroyAllWindows()