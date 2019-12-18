#!/usr/bin/env python
# coding: utf-8

# In[1]:


#to get the link of all images in a list
import os

path = 'C:\\Users\\girij\\OneDrive\\Desktop\\most important assignment\\RC'

files=[]
for r,d,f in os.walk(path):
    for file in f:
        if ".jpg" in file:
            files.append(os.path.join(r, file))

for f in files:
    print(f)


# In[2]:


# import the necessary packages
from imutils import contours
from imutils.perspective import four_point_transform
from skimage.filters import threshold_local
import numpy as np
import cv2
import imutils


# In[3]:


text_list=[]


# In[5]:


for i in range(len(files)): 
# to the new height, clone it, and resize it
    image = cv2.imread(files[i])
    ratio = image.shape[0]/500
    orig = image.copy()
    image = imutils.resize(image, height = 500)

    # convert the image to grayscale, blur it, and find edges
    # in the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)
    cv2.imshow("canny", edged)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # show the original image and the edge detected image

    # find the contours in the edged image, keeping only the
    # largest ones, and initialize the screen contour
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

    # loop over the contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        # if our approximated contour has four points, then we
        # can assume that we have found our screen
        if len(approx) == 4:
            screenCnt = approx
            break


    # show the contour (outline) of the piece of paper
    print("STEP 2: Find contours of paper")
    cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)


    # apply the four point transform to obtain a top-down
    # view of the original image
    warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

    # convert the warped image to grayscale, then threshold it
    # to give it that 'black and white' paper effect
    warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    T = threshold_local(warped, 11, offset = 10, method = "gaussian")
    warped = (warped > T).astype("uint8") * 255

    warped=imutils.resize(warped, height = 650)
    # show the original and scanned images
    cv2.imshow("warped", warped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("STEP 3: Apply perspective transform",i)
    text_list.append(imgg)


# In[166]:


cv2.imshow("img",text_list[79])
cv2.waitKey(0)
cv2.destroyAllWindows()


# In[ ]:


import pytesseract #tesseract module for extracting text form a image


# In[ ]:


pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'


# In[8]:


text_in=[]
for i in range(len(text_list)):#loop for text extraction
    text=pytesseract.image_to_string(text_list[i])
    text_in.append(text)

print(text)
