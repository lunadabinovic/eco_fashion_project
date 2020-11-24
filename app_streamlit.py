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

from cofirm_button_hack import confirm_button_example, cache_on_button_press

from eco_fashion_project.trainer import ocr_core, split_lines, get_matches, get_fiber_pct, get_pct, get_final_score
from eco_fashion_project.utils import get_pct, percentages_to_float, check_100_pct, get_score



image = Image.open('/Users/antonia/Desktop/Coding/logo_size_invert.jpg')
st.image(image, use_column_width=False)

st.markdown('# Sustainaholics')
st.write("Please upload your tag")


## user uploades an image and the model converts it to a string
st.set_option('deprecation.showfileUploaderEncoding', False)

buffer =  st.file_uploader("Choose a JPG file" ,type="JPG")

temp_file = NamedTemporaryFile(delete=False)

## prints the image
file_bytes = np.asarray(bytearray(buffer.read()), dtype=np.uint8)
opencv_image = cv2.imdecode(file_bytes, 1)
st.image(opencv_image, channels="BGR", width= 160)


if buffer is not None:
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

## gets all the matches in a dataframe
    all_matches_df = get_matches(ocr_splited, fibres_list)


## gets the tag info with percentages in a dataframne(columns = fibre and prencentages)
    tag_info = get_fiber_pct(all_matches_df,fibres_list)

    tag_info_show = tag_info.assign(hack='').set_index('hack')
    st.write(tag_info_show)

    percentage_list = percentages_to_float(tag_info)
    st.write(check_100_pct(percentage_list))

    #get the sustainability score
    #WILL NEED TO BE ADAPTED IF THE USER CHANGED THE INPUT!
    final_score = get_final_score(fiber_score_df, tag_info)
    st.write('The (initial) sustainability score is ', final_score)

## function for dropdown
    def index(start = 0):
        i = start
        while (i < len(tag_info)) == True:
            option = st.multiselect('Fiber',
                (list(fb_df_test['Material'])), list(tag_info['fiber'])[i])
            st.write('You selected:', option)


            numbers = list(range(0,101))
            numbers_list = []
            for number in numbers:
                numbers_list.append(str(number)+'%')
            option = st.multiselect('Percentage',
                    (numbers_list), list(tag_info['percentage'])[i])
            #st.write('You selected:', option)

            i += 1

    st.write("Are these the correct components and the percentages?")

    #yes = st.button('Yes')
    #no = st.button('No')
    #editing = False
    #if yes:
       # st.write('Your Final score is: ')
    #elif no or editing:
       #editing = True

    st.write('Please make the correct changes')

    index(start= 0)
    st.write(option)


    #ä@cache_on_button_press('Update')
    #def update():
      #  return True

       # index(start= 0)




           # option = st.multiselect('Fiber',
            #       (list(fb_df_test['Material'])))

          #  numbers = list(range(0,101))
          #  numbers_list = []
          #  for number in numbers:

           #    numbers_list.append(str(number)+'%')
           # option = st.multiselect('Percentage',
           #       (numbers_list))

      #  update()




    #@cache_on_button_press('Authenticate')
    # def authenticate(username, password):
     #   return username == "buddha" and password == "s4msara"

   # username = st.text_input('username')
   #password = st.text_input('password')

    #if authenticate(username, password):
     #   st.success('You are authenticated!')
     #   st.write(st.slider('Test widget')) # <- just to show that widgets work here
    #else:
       # st.error('The username or password you have entered is invalid.')



    # add = st.button('Add another component')
    #   score = st.button('Calculate my final score')


     #   if add:
     #       st.write('heb')
      #  elif score:
     #       st.write('hey')






    #i = 0
    #option = st.selectbox('Fiber',
    #(fibre))
    #st.write('You selected:', option)


            #number = st.number_input('Insert a number')
            #st.write('The current number is ', number)

