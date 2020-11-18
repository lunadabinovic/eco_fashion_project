import os
import numpy as np
import cv2

def get_data(filename):
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    img_path = os.path.join(root_path, 'raw_data', 'label_composition_images', filename)

    return img_path

def preprocessing_image(image):
    #image = cv2.imread('../raw_data/label_composition_images/IMG_1378.JPG')
    image = cv2.imread(image)
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    noise = cv2.medianBlur(grayscale,5)
    #threshold = cv2.threshold(noise, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    #threshold doesn't really work
    #dilation
    kernel = np.ones((5,5),np.uint8)
    dilate = cv2.dilate(noise, kernel, iterations = 1)
    #erosion
    kernel = np.ones((5,5),np.uint8)
    erode= cv2.erode(dilate, kernel, iterations = 1)
    #opening - erosion followed by dilation
    #definition opening(image):
    #kernel = np.ones((5,5),np.uint8)
    #return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    #canny edge detection
    #canny = cv2.Canny(threshold, 100, 200)
    #skew correction
    #definition deskew(image):
    coords = np.column_stack(np.where(erode > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = erode.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    deskew = cv2.warpAffine(erode, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    #definition sharp(image):
    #sharp= cv2.bilateralFilter(deskew,9,75,75)
    return deskew
