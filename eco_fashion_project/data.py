import os
import numpy as np
import cv2
import pandas as pd

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

def get_fibre_list(filename):
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fb_path = os.path.join(root_path, 'eco_fashion_project', 'data', filename)

    fb_keys = pd.read_csv(fb_path)
    fibres_list = fb_keys['Material'].tolist()

    return fibres_list

def get_nylon_group(fibres_list):
    nylon_group = [s for s in fibres_list if "nylon" in s or "polyamide" in s]
    return nylon_group

def get_polyester_group(fibres_list):
    polyester_group = [s for s in fibres_list if "polyester" in s]
    return polyester_group

def get_linen_group(fibres_list):
    linen_group = [s for s in fibres_list if "linen" in s]
    return linen_group

def get_hemp_group(fibres_list):
    hemp_group = [s for s in fibres_list if "hemp" in s]
    return hemp_group

def get_cotton_group(fibres_list):
    cotton_group = [s for s in fibres_list if "cotton" in s]
    return cotton_group

def get_wool_group(fibres_list):
    wool_group = [s for s in fibres_list if "wool" in s]
    return wool_group

def get_viscose_group(fibres_list):
    viscose_group = [s for s in fibres_list if "viscose" in s]
    return viscose_group

def get_leather_group(fibres_list):
    leather_group = [s for s in fibres_list if "leather" in s]
    return leather_group

def get_multi_fb_group_list(fibres_list):
    nylon_group = get_nylon_group(fibres_list)
    polyester_group = get_polyester_group(fibres_list)
    linen_group = get_linen_group(fibres_list)
    hemp_group = get_hemp_group(fibres_list)
    cotton_group = get_cotton_group(fibres_list)
    wool_group = get_wool_group(fibres_list)
    viscose_group = get_viscose_group(fibres_list)
    leather_group = get_leather_group(fibres_list)

    multi_fb_group_list = [nylon_group, polyester_group, linen_group, hemp_group, cotton_group, wool_group, viscose_group, leather_group]
    return multi_fb_group_list

def get_rest_group(fibres_list):
    rest_group = fibres_list
    multi_fb_group_list = get_multi_fb_group_list(fibres_list)
    for group in multi_fb_group_list:
        rest_group = [s for s in rest_group if s not in group]

    return rest_group
