import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# Blue
upper_bond = np.array([179, 255, 255])
lower_bond = np.array([20, 47, 0])

# Pink
upper_bond = np.array([179, 254, 255])
lower_bond = np.array([128, 62, 0])

upper_bond = np.array([179, 255, 255])
lower_bond = np.array([80, 95, 0])

snapshot = 0
snap = False

while True:
    _, frame = cap.read()
    image = cv2.flip(frame, 1)

    if snap == False:
        snap = True
        snapshot = image

    # curtain detector
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_bond, upper_bond)
    _, mask = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)
    # Invert the mask
    mask_inv = cv2.bitwise_not(mask)

    # Apply the mask to the image
    masked_image = cv2.bitwise_and(image, image, mask=mask_inv)

    # Apply the inverted mask to a white background
    white_background = snapshot
    background1 = cv2.bitwise_and(white_background, white_background, mask=mask)

    # Combine the masked image and background
    # result = cv2.add(masked_image, background1)
    result = cv2.add(background1, masked_image)

    cv2.imshow('result', result)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()
