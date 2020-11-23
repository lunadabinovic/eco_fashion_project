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
get_wool_group,get_viscose_group,get_leather_group, get_multi_fb_group_list, get_rest_group

from eco_fashion_project.trainer import ocr_core, split_lines, get_matches, get_fiber_pct, get_pct, get_final_score
from eco_fashion_project.utils import get_pct, percentages_to_float, check_100_pct, get_score

st.markdown("# CloE/ Sustainaholic")

st.write("Please upload your tag")



## user uploades an image and the model converts it to a string
st.set_option('deprecation.showfileUploaderEncoding', False)

buffer =  st.file_uploader("Choose a JPG file" ,type="JPG")

temp_file = NamedTemporaryFile(delete=False)

if buffer:
    temp_file.write(buffer.getvalue())

## passing the image to our model
    pp_image = preprocessing_image(temp_file.name)
    text = ocr_core(pp_image)
    ocr_splited= split_lines(text)

    fb_df_test = get_fibre_df('fibre_cleanedx5.csv')
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

## gets all the matches in a dataframe
    all_matches_df = get_matches(ocr_splited, fibres_list)

## gets the tag info with percentages in a dataframne(columns = fibre and prencentages)
    tag_info = get_fiber_pct(all_matches_df,fibres_list)

    tag_info_show = tag_info.assign(hack='').set_index('hack')
    st.write(tag_info_show)
    user_input = st.text_input("Are these the correct components? yes or no?")
    if user_input == 'yes':
        st.write('Your Final score is: ')
    else:
        st.write('Please make the correct changes')

    for tag in tag_info_show:
    #i = 0
        option = st.selectbox('Fiber',
        (list(tag_info_show['fiber'])))
        st.write('You selected:', option)


number = st.number_input('Insert a number')
st.write('The current number is ', number)

    #i = 0
    #option = st.selectbox('Fiber',
    #(fibre))
    #st.write('You selected:', option)



#fb_df = get_fibre_df('fibre_cleanedx5.csv')
 #       fiber_score_df = fb_df.set_index('Material')
  #      fibres_list = get_fibre_list(fb_df)
   #     percentage_list = percentages_to_float(tag_info)
        #check_100_pct(percentage_list)
    #    final_score = get_final_score(fiber_score_df, tag_info)



#st.write(pd.DataFrame{""})
#st.DataFrame({tag_})
