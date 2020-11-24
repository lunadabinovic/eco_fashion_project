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

st.markdown('''
    <img
        src="https://images.unsplash.com/photo-1489065094455-c2d576ff27a0?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=2550&q=80" id="background-image-grass">
    ''',
    unsafe_allow_html=True)

# Overall title
st.markdown("<h1 style='text-align: center; color: DarkGreen; position: relative;'>Sustainaholics</h1>", unsafe_allow_html=True)
st.text("")
st.text("")




#background-image
page_bg_img = '''
   <style>
   #background-image-grass {
        position: absolute;
        left: 0;
        top: 0;
        width: 100%;
        height: auto;
        opacity: 40%;
       }
   </style>
   '''
    # .block-container {
    #     max-width: 10000px !important;
    #  }
#
st.markdown(page_bg_img, unsafe_allow_html=True)

#image = Image.open('/Users/antonia/code/lunadabinovic/eco_fashion_project/raw_data/logo_size.jpg')
#st.image('<style=image-align:right;>image<>')
#st.image('<style= text-align: right;>image<')



st.markdown(
    """
<style>
.sidebar .sidebar-content {
    background-image: linear-gradient(#6AA071,#6AA071);
    color: white;
}
</style>
""",
    unsafe_allow_html=True,
)

# Define the Menu
st.sidebar.subheader('Select the Page')
analysis = st.sidebar.selectbox("",['Homepage', 'About'])

if analysis == 'Homepage':
    st.write("Please upload your tag")


    ## user uploades an image and the model converts it to a string
    st.set_option('deprecation.showfileUploaderEncoding', False)

    buffer = st.file_uploader("Choose a JPG file" ,type="JPG")


    ## prints the image if it is not None
    if buffer != None:
        file_bytes = np.asarray(bytearray(buffer.read()), dtype=np.uint8)
        opencv_image = cv2.imdecode(file_bytes, 1)
        st.image(opencv_image, channels="BGR", width= 160)
        temp_file = NamedTemporaryFile(delete=False)
    else:
        st.warning('No file has been selected')

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



if analysis == 'About':
    st.markdown("<h3 style='text-align: center;'>About Sustainaholics</h3>", unsafe_allow_html=True)
    st.write('Sustainaholics came about thanks to Le Wagon Data Science Bootcamp where Antonia, Luna and Charlotte met. \
        Charlotte, mom of 2, is our coding superstar and mood-uplifter. Luna (humanitarian engineer and project leader) \
        and Antonia (soon to be marine biologist) are the perfect duo, making every individual assignment, a team effort since\
        day one, ensuring a fun environment for everyone! We are all passionate about the environment and concerned about the impact\
        of fashion on our planet. We wanted to create an app that makes it easier for consumers to become more aware of the environmental impact \
        clothes can have but also give them the possibility to make better informed choices.')
    st.write('Sustainaholics is truly about unity and supporting each other. We believe that effective change can only happen collectively \
        and we hope to be a part of this change.')

    st.markdown("<h3 style='text-align: center;'>About our sustainability scores</h3>", unsafe_allow_html=True)
    st.write('We are using two different data sources to compute the environmental scores of your clothes: \
        MadeBy Environmental Benchmark for Fibres and Amberoot’s Fabric Sustainability Score. Your sustainability score is \
        then calculated using the weights (percentages) of the different fibres composing your item of clothing.')

    st.markdown("<h3 style='text-align: center;'>About the future improvements</h3>", unsafe_allow_html=True)
    st.write('OCR improvements: We are aware that the accuracy of our OCR model could be improved.\
     As such, this could be done by training a model based on the user input compared to the original image.')
    st.write('Geolocalisation: If an item is made in Bangladesh for example and you are buying it in Portugal, it would not have the same \
    environmental impact as if you were buying it in Bangladesh. Therefore, integrating the added impact based on the location of \
    the buyer according to where the item was produced, could also be an interesting feature to add.')
    st.write('Business Opportunities: Perhaps a functionality could be integrated where the user is asked\
    for or what they are looking to buy (ie: party dress, pants etc.) and is recommended different sustainable \
    sources/shops, to buy such an item.')



