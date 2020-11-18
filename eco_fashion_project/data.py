import os

def get_data(filename):
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    img_path = os.path.join(root_path, 'raw_data', 'label_composition_images', filename)

    return img_path
