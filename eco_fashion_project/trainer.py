from eco_fashion_project.data import get_data, preprocessing_image, get_fibre_df, get_fibre_list, get_multi_fb_group_list, get_rest_group, get_brand_transp_df, get_brand_list
from eco_fashion_project.utils import get_pct, percentages_to_float, check_100_pct, get_score
import os
import pandas as pd


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

def split_lines(text):
    text_per_line = text.splitlines()
    return text_per_line

def get_matches(ocr_splitted, fibres_list):
    all_matches = []
    for fibre in fibres_list:
        matching = [s.lower() for s in ocr_splitted if fibre in s.lower()]
        if matching:
            matched = [fibre, matching]
            all_matches.append(matched)

    all_matches_df = pd.DataFrame(all_matches)
    return all_matches_df


def get_fiber_pct(df, fibres_list):
    if not df.empty:
        ind_df = df.set_index(0)
        multi_fb_group_list = get_multi_fb_group_list(fibres_list)
        rest_group = get_rest_group(fibres_list)

        tag_info = pd.DataFrame(columns = ["fiber", "percentage"])

        for group in multi_fb_group_list:
            if df[0].isin(group).any() == True:
                grouped_fibres = df[0][df[0].isin(group)]

                fb_key = max(grouped_fibres, key=len)
                if fb_key == "polyamide" and grouped_fibres.iloc[0] == 'nylon':
                    fb_key = 'nylon'

                pct = get_pct(ind_df, fb_key)
                tag_info.loc[len(tag_info)] = [fb_key,pct]

        if df[0].isin(rest_group).any() == True:
            for match in df[0][df[0].isin(rest_group)]:
                fb_key = match
                pct = get_pct(ind_df, fb_key)
                tag_info.loc[len(tag_info)] = [fb_key,pct]

        return tag_info


def get_final_score(fiber_score_df, df):
    if df is not None:
        tag_score_df = df.set_index('fiber')
        tag_score_df['share'] = percentages_to_float(df)
        tag_score_df['score'] = get_score(fiber_score_df, df)
        tag_score_df['share_score'] = tag_score_df['share'] * tag_score_df['score']
        sust_score = round(tag_score_df.sum(axis = 0, skipna = True)['share_score'],3)
        return sust_score

def get_overall_pct_brand_score(brand_score_df, brand):
    '''returns a float equal to the overall percentage fashion transparency index of the brand'''
    if brand:
        overall_pct_brand_score = brand_score_df.loc[brand]["FASHION TRANSPARENCY INDEX 2020 (%)"]
        return overall_pct_brand_score

def get_pct_brand_scores_per_section(brand_score_df, brand):
    '''returns a Series of 5 floats equal to the percentages of the 5 sections of the fashion transparency index of the brand'''
    if brand:
        pct_brand_score_per_section = brand_score_df.loc[brand]["1. POLICY & COMMITMENTS":"FASHION TRANSPARENCY INDEX 2020 (%)":2]
        #pct_brand_score_per_section = brand_score_df.loc[brand][1:11:2]
        return pct_brand_score_per_section

def get_pct_brand_score_for_section_1(brand_score_df, brand):
    '''returns a float equal to the percentage of the first section of the fashion transparency index of the brand'''
    if brand:
        pct_brand_score_for_section_1 = brand_score_df.loc[brand]["1. POLICY & COMMITMENTS"]
        return pct_brand_score_for_section_1

def get_pct_brand_score_for_section_2(brand_score_df, brand):
    '''returns a float equal to the percentage of section 2 of the fashion transparency index of the brand'''
    if brand:
        pct_brand_score_for_section_2 = brand_score_df.loc[brand]["2. GOVERNANCE"]
        return pct_brand_score_for_section_2

def get_pct_brand_score_for_section_3(brand_score_df, brand):
    '''returns a float equal to the percentage of section 3 of the fashion transparency index of the brand'''
    if brand:
        pct_brand_score_for_section_3 = brand_score_df.loc[brand]["3. TRACEABILITY"]
        return pct_brand_score_for_section_3

def get_pct_brand_score_for_section_4(brand_score_df, brand):
    '''returns a float equal to the percentage of section 4 of the fashion transparency index of the brand'''
    if brand:
        pct_brand_score_for_section_4 = brand_score_df.loc[brand]["4. KNOW, SHOW & FIX"]
        return pct_brand_score_for_section_4

def get_pct_brand_score_for_section_5(brand_score_df, brand):
    '''returns a float equal to the percentage of section 5 of the fashion transparency index of the brand'''
    if brand:
        pct_brand_score_for_section_5 = brand_score_df.loc[brand]["5. SPOTLIGHT ISSUES (CONDITIONS, CONSUMPTION, COMPOSITION, CLIMATE)"]
        return pct_brand_score_for_section_5


if __name__ == "__main__":

    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    img_folder_path = os.path.join(root_path, 'raw_data', 'label_composition_images')
    images = os.listdir(img_folder_path)
    images = [image for image in images if not image.startswith(".")]

    fb_df = get_fibre_df('fibre_cleanedx4.csv')
    fiber_score_df = fb_df.set_index('Material')
    fibres_list = get_fibre_list(fb_df)

    brand_score_df = get_brand_transp_df('brands_final_score.xlsx')
    brand_list = get_brand_list(brand_score_df)

    print("ocr_core (image_to_string):")
    for image in images:
        #image = 'IMG_1388.JPG'
        img_used = get_data(image)
        img_preproc = preprocessing_image(img_used)
        ocr_result = ocr_core(img_preproc)
        ocr_splitted = split_lines(ocr_result)

        print(f"OCR split per line: {image}:")
        print(ocr_splitted)
        '''
        print("ocr_ext (image_to_data):")
        print(ocr_ext(img_preproc))
        '''
        all_matches_df = get_matches(ocr_splitted, fibres_list)
        tag_info = get_fiber_pct(all_matches_df, fibres_list)
        print(f"tag info for image: {image}:")
        print(tag_info)

        percentage_list = percentages_to_float(tag_info)
        print(check_100_pct(percentage_list))
        final_score = get_final_score(fiber_score_df, tag_info)
        print(f"sustainability score for image: {image}: {final_score}")

    print(f"Brand list: {brand_list}")
    #brand = input("For which brand would you like to get the fashion transparency index scores? (Pick from brand_list)")
    #brand = 'Abercrombie & Fitch'
    brand = "Versace"
    print(f"Overall brand score {brand} (%): {get_overall_pct_brand_score(brand_score_df, brand)}")
    print(f"Overall brand score {brand} (%): {float(get_overall_pct_brand_score(brand_score_df, brand))}")
    print(f"Brand score per section {brand} (%): {get_pct_brand_scores_per_section(brand_score_df, brand)}")
