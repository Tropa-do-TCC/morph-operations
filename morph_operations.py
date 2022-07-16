import cv2
import numpy as np

def dilatation(img, kernel, iterations_number=1):
    dilation_img = cv2.dilate(img,kernel,iterations = iterations_number)
    return dilation_img

def erosion(img, kernel, iterations_number=1):
    erosion_img = cv2.erode(img,kernel,iterations = iterations_number)
    return erosion_img

def opening(img, kernel):
    opening_img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    return opening_img

def closing(img, kernel):
    closing_img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    return closing_img