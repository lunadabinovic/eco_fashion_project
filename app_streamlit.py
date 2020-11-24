import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import string
import os
import cv2
from os.path import isfile
from os.path import dirname
import seaborn as sns
from tempfile import NamedTemporaryFile
#from tensorflow.keras.preprocessing_image import load_img

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

from eco_fashion_project.data import get_data, preprocessing_image, get_fibre_list,\
get_fibre_df, get_nylon_group, get_polyester_group,get_linen_group,get_hemp_group,get_cotton_group,\
get_wool_group,get_viscose_group,get_leather_group, get_multi_fb_group_list, get_rest_group,\
get_brand_transp_df, get_brand_list

from eco_fashion_project.trainer import ocr_core, split_lines, get_matches, get_fiber_pct, get_pct, get_final_score,\
get_overall_pct_brand_score, get_pct_brand_scores_per_section
from eco_fashion_project.utils import get_pct, percentages_to_float, check_100_pct, get_score

st.markdown("# Sustainaholic")

st.write("Please upload your tag")


## user uploades an image and the model converts it to a string
st.set_option('deprecation.showfileUploaderEncoding', False)

buffer =  st.file_uploader("Choose a JPG file" ,type="JPG")

temp_file = NamedTemporaryFile(delete=False)

## prints the image
file_bytes = np.asarray(bytearray(buffer.read()), dtype=np.uint8)
opencv_image = cv2.imdecode(file_bytes, 1)
st.image(opencv_image, channels="BGR", width= 160)


if buffer:
    temp_file.write(buffer.getvalue())

## passing the image to our model
    pp_image = preprocessing_image(temp_file.name)
    text = ocr_core(pp_image)
    ocr_splited= split_lines(text)

    fb_df_test = get_fibre_df('fibre_cleanedx5.csv')
    fiber_score_df = fb_df_test.set_index('Material')
    fibres_list = get_fibre_list(fb_df_test)

## defining all the groupos with the functions from data.py
    nylon_group = get_nylon_group(fibres_list)
    polyester_group = get_polyester_group(fibres_list)
    linen_group = get_linen_group(fibres_list)
    hemp_group = get_hemp_group(fibres_list)
    cotton_group = get_cotton_group(fibres_list)
    wool_group = get_wool_group(fibres_list)
    viscose_group = get_viscose_group(fibres_list)
    leather_group = get_leather_group(fibres_list)
    multi_fb_group_list = get_multi_fb_group_list(fibres_list)
    rest_group = get_rest_group(fibres_list)

## get brand scores
    brand_score_df = get_brand_transp_df('brands_final_score.xlsx')
    brand_list = get_brand_list(brand_score_df)


## gets all the matches in a dataframe
    all_matches_df = get_matches(ocr_splited, fibres_list)


## gets the tag info with percentages in a dataframne(columns = fibre and prencentages)
    tag_info = get_fiber_pct(all_matches_df,fibres_list)

    tag_info_show = tag_info.assign(hack='').set_index('hack')
    st.write(tag_info_show)

    percentage_list = percentages_to_float(tag_info)
    st.write(check_100_pct(percentage_list))


## function for dropdown
    def index(start = 0):
        i = start
        while (i < len(tag_info)) == True:
            option = st.multiselect('Fiber',
                (list(fb_df_test['Material'])), list(tag_info['fiber'])[i])
            #st.write('You selected:', option)
            #ad_tag_info['fiber'][i] = option
            ad_fibres.append(option[0])


            numbers = list(range(0,101))
            numbers_list = []
            for number in numbers:
                numbers_list.append(str(number)+'%')
            option = st.multiselect('Percentage',
                    (numbers_list), list(tag_info['percentage'])[i])
            #st.write('You selected:', option)
            #ad_tag_info['percentage'][i] = option
            ad_percentages.append(option[0])

            i += 1

    def add_components(start = len(tag_info)):
        i = start
        # CHECK HOW CHECKBOX CLICKED :
        #if i :
        option = st.multiselect('Fiber',
            (list(fb_df_test['Material'])), list(fb_df_test['Material'])[0], key=f"fiber{i}")
        #st.write('You selected:', option)
        #ad_tag_info['fiber'][i] = option
        ad_fibres.append(option[0])


        numbers = list(range(0,101))
        numbers_list = []
        for number in numbers:
            numbers_list.append(str(number)+'%')
        option = st.multiselect('Percentage',
                (numbers_list), numbers_list[0], key=f"pct{i}")
        #st.write('You selected:', option)
        #ad_tag_info['percentage'][i] = option
        ad_percentages.append(option[0])

        #i += 1

    #TO BE COMPLETED:
    def add_input_field_and_checkbox(k):
        add_components(start = len(tag_info))
        k += 1
        #if st.checkbox('Add another component', key=f"{k}")


    st.write("Are these the correct components and percentages?")
    if st.checkbox('Yes'):
        #get the sustainability score
        final_score = get_final_score(fiber_score_df, tag_info)
        st.write('The sustainability score is ', final_score)
    elif st.checkbox('No'):
        #ad_tag_info = tag_info
        ad_fibres = []
        ad_percentages = []
        st.write('Please make the correct changes')
        index(start = 0)
        k = 1

        if st.checkbox('Add another component', key=f"{k}"):
            add_components(start = len(tag_info))
            #st.write('working?')
            # ADD ANOTHER COMPONENT IN A LOOP
            #add_input_field_and_checkbox(k)

        if st.button('Calculate my final score'):
            d = {'fiber': ad_fibres, 'percentage': ad_percentages}
            ad_tag_info = pd.DataFrame(data=d)
            ad_tag_info_show = ad_tag_info.assign(hack='').set_index('hack')
            st.write(ad_tag_info_show)

            ad_percentage_list = percentages_to_float(ad_tag_info)
            st.write(check_100_pct(ad_percentage_list))
            ad_sust_score = get_final_score(fiber_score_df, ad_tag_info)
            st.write('The sustainability score is ', ad_sust_score)

            #st.write('hey')
            # Change the entry at (row, col) to the given value
            #tag_info.values[row][col] = value

    if st.checkbox('Show fashion transparency index for brand'):
        brand = st.multiselect('Brand',
            (brand_list), brand_list[0])
        st.write("Overall brand score (%): ", get_overall_pct_brand_score(brand_score_df, brand))
        # TO BE COMPLETED
        st.write("Brand score per section (%): ", get_pct_brand_scores_per_section(brand_score_df, brand))






    #i = 0
    #option = st.selectbox('Fiber',
    #(fibre))
    #st.write('You selected:', option)


            #number = st.number_input('Insert a number')
            #st.write('The current number is ', number)

