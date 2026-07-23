import cv2
import numpy as np

#Set up webcame capture
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: could not open the webcam")
    exit()

while True:
    # Capture the frame by frame
    ret, frame = cap.read()

    if not ret:
        print("Error: failed to capture the image")
        break

    #Convert to HSV for color filtering
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #Define the range for skin color in hsv
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)

    #Create a mask to detect skin color
    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    #Apply the mask to the frame
    result = cv2.bitwise_or(frame, frame, mask=mask)

    #Find contours (hand shape) in the masked image
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #If contours are found, draw them
    if contours:
        max_contour = max(contours, key=cv2.contourArea) #Get the largest contour
        if cv2.contourArea(max_contour) > 500: #Ignore small contours
            #Draw the bounding vox around the detected hand
            x, y, w, h = cv2.boundingRect(max_contour)
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)

            #Get the center of the hand for further tracking or interaction
            center_x = int(x + w / 2)
            center_y = int(y + h / 2)
            cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1) #Red dor at the center

    #Display the original and result frames
    cv2.imshow('Original Frame', frame)
    cv2.imshow('Filtered frame', result)

    #Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()