import cv2
import numpy as np


cap = cv2.VideoCapture(0)

class Removebg():
    def __init__(self,upper_bond,lower_bond):
        self.upper_bond = upper_bond
        self.lower_bond = lower_bond
        self.image = None

    def remove(self):
        img1 = self.image
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        img2 = cv2.flip(self.image,1)
        img2 = cv2.resize(img2,(self.image.shape[1],self.image.shape[0]))

        mask = cv2.inRange(hsv, np.array(self.lower_bond), np.array(self.upper_bond))
        # Invert the mask
        mask = cv2.bitwise_not(mask)
        # Use the mask to create a masked version of image 2
        res = cv2.bitwise_and(img2, img2, mask=mask)
        # Use the mask to create a masked version of image 1
        # img1 = cv2.bitwise_and(img1, img1, mask=cv2.bitwise_not(mask))
        # Combine the two images
        result = cv2.addWeighted(img1, 1, res, 1, 0)

        return result

rb = Removebg(upper_bond=[179,255,255],lower_bond=[20,47,0])

# Blue
upper_bond= np.array([179,255,255])
lower_bond= np.array([20,47,0])

# Pink
upper_bond= np.array([179,254,255])
lower_bond= np.array([128,62,0])


snapshot = 0
snap = False

while True:
    _,frame = cap.read()
    image = cv2.flip(frame,1)
    rb.image = cv2.flip(frame,1)

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