from eco_fashion_project.data import get_data, preprocessing_image
import os

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract


def ocr_core(image):
    """
    This function will handle the core OCR processing of images (image_to_string).
    This function works when an image is passed, when a file is passed as an argument,
    the function would need to be adapted as:
    text = pytesseract.image_to_string(Image.open(filename))
    """
    text = pytesseract.image_to_string(image)
    return text

'''
def ocr_ext(filename):
    """
    Get verbose data including boxes, confidences, line and page numbers (image_to_data).
    """
    text = pytesseract.image_to_data(Image.open(filename))
    return text
'''

if __name__ == "__main__":

    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    img_folder_path = os.path.join(root_path, 'raw_data', 'label_composition_images')
    images = os.listdir(img_folder_path)

    print("ocr_core (image_to_string):")
    for image in images:
        #image = 'IMG_1378.JPG'
        img_used = get_data(image)
        img_preproc = preprocessing_image(img_used)
        print(f"{image}:")
        print(ocr_core(img_preproc))
        '''
        print("ocr_ext (image_to_data):")
        print(ocr_ext(img_preproc))
        '''
