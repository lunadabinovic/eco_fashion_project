from eco_fashion_project.data import get_data

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract


def ocr_core(filename):
    """
    This function will handle the core OCR processing of images (image_to_string).
    """
    text = pytesseract.image_to_string(Image.open(filename))
    return text

def ocr_ext(filename):
    """
    Get verbose data including boxes, confidences, line and page numbers (image_to_data).
    """
    text = pytesseract.image_to_data(Image.open(filename))
    return text

if __name__ == "__main__":
    img_used = get_data('images.png')

    print("ocr_core (image_to_string):")
    print(ocr_core(img_used))
    print("ocr_ext (image_to_data):")
    print(ocr_ext(img_used))
