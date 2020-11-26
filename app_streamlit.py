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
import plotly.express as px
import plotly.graph_objs as go
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
get_overall_pct_brand_score, get_pct_brand_scores_per_section, get_pct_brand_score_for_section_1, get_pct_brand_score_for_section_2,\
get_pct_brand_score_for_section_3, get_pct_brand_score_for_section_4, get_pct_brand_score_for_section_5
from eco_fashion_project.utils import get_pct, percentages_to_float, check_100_pct, get_score,\
convert_5scale_to_emoji, convert_pct_to_emoji


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


#st.sidebar.image("https://dewey.tailorbrands.com/production/brand_version_mockup_image/659/4176770659_a3bf8455-bde9-4cb3-aa49-6dc1f30ea7b5.png?cb=1606149896", width=150)
#st.sidebar.image("https://dewey.tailorbrands.com/production/brand_version_mockup_image/659/4176770659_a3bf8455-bde9-4cb3-aa49-6dc1f30ea7b5.png?cb=1606149896", use_column_width=True)

# Define the Menu
st.sidebar.subheader('Select the Page')
analysis = st.sidebar.selectbox("",['Sustainability score', 'Brand transparency', 'About'])


page_bg_img = '''
<style>
.reportview-container {
    width: 100%;
    height: 100%;
    min-width: 100%;
    min-height: 100%;
    position: relative;
    }

.reportview-container::before {
    background-image: url(https://images.unsplash.com/photo-1489065094455-c2d576ff27a0?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=2550&q=80);
    background-size: cover;
    content: "";
    display: block;
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -2;
    opacity: 0.4;
    }

.reportview-container::after {
    background-color: #81a385;
    content: "";
    display: block;
    position: absolute;
    top: 0px;
    left: 0px;
    width: 100%;
    height: 100%;
    z-index: -1;
    opacity: 0.4;
    }
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)

hc1, hc2, hc3 = st.beta_columns((1,2,1))
hc2.image("https://dewey.tailorbrands.com/production/brand_version_mockup_image/659/4176770659_a3bf8455-bde9-4cb3-aa49-6dc1f30ea7b5.png?cb=1606149896", use_column_width=True)
#st.image("https://dewey.tailorbrands.com/production/brand_version_mockup_image/659/4176770659_a3bf8455-bde9-4cb3-aa49-6dc1f30ea7b5.png?cb=1606149896", width=200)

#st.markdown("<h1 style='text-align: center; color: #406144; position: relative; padding-bottom: 50px'>Sustainaholics</h1>", unsafe_allow_html=True)

#image = Image.open('/Users/antonia/code/lunadabinovic/eco_fashion_project/raw_data/logo_size.jpg')
#st.image('<style=image-align:right;>image<>')
#st.image('<style= text-align: right;>image<')


if analysis == 'Sustainability score':
    st.markdown("<h1 style='text-align: center; color: #406144; position: relative; padding-bottom: 50px'>How sustainable are the clothes you like?</h1>", unsafe_allow_html=True)
    st.write("Please upload your clothing tag")


    ## user uploades an image and the model converts it to a string
    st.set_option('deprecation.showfileUploaderEncoding', False)

    buffer = st.file_uploader("Choose a file" ,type=["jpg", "ipeg", "jpeg", "png"] )

    c1, c2, c3, c4 = st.beta_columns((1,2,2,1))

    ## prints the image if it is not None
    if buffer != None:
        file_bytes = np.asarray(bytearray(buffer.read()), dtype=np.uint8)
        opencv_image = cv2.imdecode(file_bytes, 1)
        c2.image(opencv_image, channels="BGR", width= 160)
        temp_file = NamedTemporaryFile(delete=False)
    else:
        st.warning('No tag has been selected')


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

        if isinstance(tag_info, pd.DataFrame):

            tag_info_show = tag_info.assign(hack='').set_index('hack')
            c3.write(tag_info_show)

            percentage_list = percentages_to_float(tag_info)
            st.write(check_100_pct(percentage_list))



        ## function for dropdown
            def index(start = 0):
                i = start
                col1, col2 = st.beta_columns((2,1))
                while (i < len(tag_info)) == True:
                    option = col1.multiselect('Fiber',
                        (list(fb_df_test['Material'])), list(tag_info['fiber'])[i])
                    ad_fibres.append(option[0])


                    numbers = list(range(0,101))
                    numbers_list = []
                    for number in numbers:
                        numbers_list.append(str(number)+'%')
                    option = col2.multiselect('Percentage',
                        (numbers_list), list(tag_info['percentage'])[i])
                    ad_percentages.append(option[0])

                    i += 1

            def add_components(start = len(tag_info)):
                i = start
                col1, col2 = st.beta_columns((2,1))
                option = col1.multiselect('Fiber',
                    (list(fb_df_test['Material'])), list(fb_df_test['Material'])[0], key=f"fiber{i}")
                ad_fibres.append(option[0])

                numbers = list(range(0,101))
                numbers_list = []
                for number in numbers:
                    numbers_list.append(str(number)+'%')
                option = col2.multiselect('Percentage',
                        (numbers_list), numbers_list[0], key=f"pct{i}")
                ad_percentages.append(option[0])



            st.write("Are these the correct components and percentages?")
            if st.checkbox('Yes'):
                #get the sustainability score
                final_score = get_final_score(fiber_score_df, tag_info)

                sc1, sc2, sc3, sc4, sc5 = st.beta_columns((1,1,4,1,1))

                sc2.markdown(convert_5scale_to_emoji(final_score))
                sc3.markdown(f"<div style='font-size: 20px; font-weight: bold; color: #406144;'>Sustainability score: {final_score}/5</div>", unsafe_allow_html=True)
                sc4.markdown(convert_5scale_to_emoji(final_score))
                #st.write('Sustainability score: ', convert_5scale_to_emoji(final_score), final_score,"/5")
            elif st.checkbox('No'):
                ad_fibres = []
                ad_percentages = []
                st.write('Please make the correct changes')
                #col1, col2 = st.beta_columns((2,1))
                index(start = 0)
                k = 1

                if st.checkbox('Add another component', key=f"{k}"):
                    add_components(start = len(tag_info))
                    # ADD ANOTHER COMPONENT IN A LOOP
                    #add_input_field_and_checkbox(k)

                if st.button('Calculate sustainability score'):
                    d = {'fiber': ad_fibres, 'percentage': ad_percentages}
                    ad_tag_info = pd.DataFrame(data=d)
                    ad_tag_info_show = ad_tag_info.assign(hack='').set_index('hack')
                    st.write(ad_tag_info_show)

                    ad_percentage_list = percentages_to_float(ad_tag_info)
                    st.write(check_100_pct(ad_percentage_list))
                    ad_sust_score = get_final_score(fiber_score_df, ad_tag_info)
                    sc1, sc2, sc3, sc4, sc5 = st.beta_columns((1,1,4,1,1))
                    sc2.markdown(convert_5scale_to_emoji(ad_sust_score))
                    sc3.markdown(f"<div style='font-size: 20px; font-weight: bold; color: #406144;'>Sustainability score: {ad_sust_score}/5</div>", unsafe_allow_html=True)
                    sc4.markdown(convert_5scale_to_emoji(ad_sust_score))
                    #st.write('Sustainability score: ', convert_5scale_to_emoji(ad_sust_score), ad_sust_score,"/5")

        else:
            st.warning('Sorry our model did not detect text on your image. Please input the components manually')
            if st.checkbox('Add component'):

                ## first one
                ad_fibres = []
                ad_percentages = []

                col1, col2 = st.beta_columns((2,1))
                option = col1.multiselect('Fiber',
                    (list(fb_df_test['Material'])), fb_df_test['Material'][0] ,key=123)
                ad_fibres.append(option[0])

                numbers = list(range(0,101))
                numbers_list = []
                for number in numbers:
                    numbers_list.append(str(number)+'%')
                option = col2.multiselect('Percentage',
                    (numbers_list), numbers_list[0], key=124)
                ad_percentages.append(option[0])

                ## second one
                col1, col2 = st.beta_columns((2,1))
                option = col1.multiselect('Fiber',
                    (list(fb_df_test['Material'])), fb_df_test['Material'][0],key=125)
                ad_fibres.append(option[0])

                numbers = list(range(0,101))
                numbers_list = []
                for number in numbers:
                    numbers_list.append(str(number)+'%')
                option = col2.multiselect('Percentage',
                    (numbers_list),numbers_list[0], key=126)
                ad_percentages.append(option[0])

                ## third one
                col1, col2 = st.beta_columns((2,1))
                option = col1.multiselect('Fiber',
                    (list(fb_df_test['Material'])), fb_df_test['Material'][0],key=126)
                ad_fibres.append(option[0])

                numbers = list(range(0,101))
                numbers_list = []
                for number in numbers:
                    numbers_list.append(str(number)+'%')
                option = col2.multiselect('Percentage',
                    (numbers_list),numbers_list[0], key=127)
                ad_percentages.append(option[0])

                ## fourth one
                col1, col2 = st.beta_columns((2,1))
                option = col1.multiselect('Fiber',
                    (list(fb_df_test['Material'])), fb_df_test['Material'][0],key=128)
                ad_fibres.append(option[0])

                numbers = list(range(0,101))
                numbers_list = []
                for number in numbers:
                    numbers_list.append(str(number)+'%')
                option = col2.multiselect('Percentage',
                    (numbers_list), numbers_list[0], key=129)
                ad_percentages.append(option[0])



            if st.checkbox('Calculate sustainability score'):
                d = {'fiber': ad_fibres, 'percentage': ad_percentages}
                ad_tag_info = pd.DataFrame(data=d)
                ad_tag_info_show = ad_tag_info.assign(hack='').set_index('hack')
                st.write(ad_tag_info_show)

                ad_percentage_list = percentages_to_float(ad_tag_info)
                st.write(check_100_pct(ad_percentage_list))
                ad_sust_score = get_final_score(fiber_score_df, ad_tag_info)
                sc1, sc2, sc3, sc4, sc5 = st.beta_columns((1,1,4,1,1))
                sc2.markdown(convert_5scale_to_emoji(ad_sust_score))
                sc3.markdown(f"<div style='font-size: 20px; font-weight: bold; color: #406144;'>Sustainability score: {ad_sust_score}/5</div>", unsafe_allow_html=True)
                sc4.markdown(convert_5scale_to_emoji(ad_sust_score))
                #st.write('Sustainability score: ', convert_5scale_to_emoji(ad_sust_score), ad_sust_score,"/5")
                #st.write(convert_5scale_to_emoji(ad_sust_score))



if analysis == 'Brand transparency':
    st.markdown("<h1 style='text-align: center; color: #406144; position: relative; padding-bottom: 50px'>How sustainable is the brand you like?</h1>", unsafe_allow_html=True)
    brand_score_df = get_brand_transp_df('brands_final_score.xlsx')
    brand_list = get_brand_list(brand_score_df)
    st.markdown('Have a look at the sustainability score for your favorite brands')
    #if st.checkbox('Show fashion transparency index for brand'):
    brand = st.selectbox('Brands selection',
    (brand_list))
    brand_score = float(get_overall_pct_brand_score(brand_score_df, brand))
    brand_score_pct = round(brand_score * 100)
    #st.write("Overall brand score (%): ", convert_pct_to_emoji(brand_score), brand_score_pct, " %")
    sc1, sc2, sc3, sc4, sc5 = st.beta_columns((1,1,4,1,1))

    sc2.markdown(convert_pct_to_emoji(brand_score))
    sc3.markdown(f"<div style='font-size: 20px; font-weight: bold; color: #406144;'>Overall brand score (FTI): {brand_score_pct} %</div>", unsafe_allow_html=True)
    sc4.markdown(convert_pct_to_emoji(brand_score))

    ## Graph visualisation
    sec_1= get_pct_brand_score_for_section_1(brand_score_df, brand)
    sec_2= get_pct_brand_score_for_section_2(brand_score_df, brand)
    sec_3= get_pct_brand_score_for_section_3(brand_score_df, brand)
    sec_4= get_pct_brand_score_for_section_4(brand_score_df, brand)
    sec_5= get_pct_brand_score_for_section_5(brand_score_df, brand)
    chart_dict = {"Policy & Commitments (%)":sec_1, "Governance (%)": sec_2, "Traceability (%)": sec_3, "Know, show, fix (%)": sec_4, "Spotlight Issues (%)**": sec_5}
    chart_matrix = np.zeros((5,5))
    counter = 0
    for k,v in chart_dict.items():
        chart_matrix[counter,counter] = v
        counter += 1
    chart_dict_df = pd.DataFrame(chart_matrix, index = chart_dict.keys(), columns = chart_dict.keys())
    st.bar_chart(chart_dict_df)
            #st.write(chart_dict_df)
    st.write("** Spotlight issues refer to: Conditions, Consumption, Climate, Composition")
            ##For display in the same table
            #columns = list(chart_dict.keys())
            #values = list(chart_dict.values())
            #arr_len = len(values)
            #chart_df = pd.DataFrame(np.array(values, dtype=object).reshape(1, arr_len), columns=columns)
            #st.write(chart_df)


    st.write("Want to know more ? Then click on the following sections to visualise how every brand scores based on the different categories")
    brand_score_df.reset_index(inplace = True)
    brand_score_df.rename(columns = {'1. POLICY & COMMITMENTS': 'Policy & Commitments', '2. GOVERNANCE': 'Governance','3. TRACEABILITY': 'Traceability','4. KNOW, SHOW & FIX': 'Know, Show & Fix','5. SPOTLIGHT ISSUES (CONDITIONS, CONSUMPTION, COMPOSITION, CLIMATE)':'Spotlight Issues'}, inplace = True)
    if st.checkbox('Policy & Commitments'):
        fig = px.scatter(brand_score_df, x='FASHION TRANSPARENCY INDEX 2020 (%)', y='Policy & Commitments', hover_data = ["Brand Name"])
        fig.update(layout= dict(
            legend= dict(orientation='h', y= 1.1, x=0.5),
            annotations= [go.layout.Annotation(text= brand, x= brand_score_df[brand_score_df["Brand Name"].str.startswith(brand)]["FASHION TRANSPARENCY INDEX 2020 (%)"].iloc[0], y=brand_score_df[brand_score_df["Brand Name"].str.startswith(brand)]["Policy & Commitments"].iloc[0])]))
        st.plotly_chart(fig)
    if st.checkbox('Governance'):
        fig = px.scatter(brand_score_df, x='FASHION TRANSPARENCY INDEX 2020 (%)', y='Governance', hover_data = ["Brand Name"])
        fig.update(layout= dict(
            legend= dict(orientation='h', y= 1.1, x=0.5),
            annotations= [go.layout.Annotation(text= brand, x= brand_score_df[brand_score_df["Brand Name"].str.startswith(brand)]["FASHION TRANSPARENCY INDEX 2020 (%)"].iloc[0], y=brand_score_df[brand_score_df["Brand Name"].str.startswith(brand)]['Governance'].iloc[0])]))
        st.plotly_chart(fig)
    if st.checkbox('Traceability'):
        fig = px.scatter(brand_score_df, x='FASHION TRANSPARENCY INDEX 2020 (%)', y='Traceability', hover_data = ["Brand Name"])
        fig.update(layout= dict(
            legend= dict(orientation='h', y= 1.1, x=0.5),
            annotations= [go.layout.Annotation(text= brand, x= brand_score_df[brand_score_df["Brand Name"].str.startswith(brand)]["FASHION TRANSPARENCY INDEX 2020 (%)"].iloc[0], y=brand_score_df[brand_score_df["Brand Name"].str.startswith(brand)]['Traceability'].iloc[0])]))
        st.plotly_chart(fig)
    if st.checkbox('Know, Show & Fix'):
        fig = px.scatter(brand_score_df, x='FASHION TRANSPARENCY INDEX 2020 (%)', y='Know, Show & Fix', hover_data = ["Brand Name"])
        fig.update(layout= dict(
            legend= dict(orientation='h', y= 1.1, x=0.5),
            annotations= [go.layout.Annotation(text= brand, x= brand_score_df[brand_score_df["Brand Name"].str.startswith(brand)]["FASHION TRANSPARENCY INDEX 2020 (%)"].iloc[0], y=brand_score_df[brand_score_df["Brand Name"].str.startswith(brand)]['Know, Show & Fix'].iloc[0])]))
        st.plotly_chart(fig)
    if st.checkbox('Spotlight Issues'):
        fig = px.scatter(brand_score_df, x='FASHION TRANSPARENCY INDEX 2020 (%)', y='Spotlight Issues', hover_data = ["Brand Name"])
        fig.update(layout= dict(
            legend= dict(orientation='h', y= 1.1, x=0.5),
            annotations= [go.layout.Annotation(text= brand, x= brand_score_df[brand_score_df["Brand Name"].str.startswith(brand)]["FASHION TRANSPARENCY INDEX 2020 (%)"].iloc[0], y=brand_score_df[brand_score_df["Brand Name"].str.startswith(brand)]['Spotlight Issues'].iloc[0])]))
        st.plotly_chart(fig)




if analysis == 'About':
    #st.markdown("<h1 style='text-align: center; color: #406144; position: relative; padding-bottom: 50px'>How sustainable are the clothes you like?</h1>", unsafe_allow_html=True)
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
    st.write('Our sustainability score for brands comes from the Fashion Transparency Index available here: https://www.fashionrevolution.org/about/transparency/. We are only accounting for the 2020 values.')
    if st.checkbox('Display fibre data set', False):
        fb_df_test = get_fibre_df('fibre_cleanedx5.csv')
        st.dataframe(fb_df_test)
    if st.checkbox('Display environmental score of brands', False):
        brand_score_df = get_brand_transp_df('brands_final_score.xlsx')
        st.dataframe(brand_score_df)

    st.markdown("<h3 style='text-align: center;'>About the future improvements</h3>", unsafe_allow_html=True)
    st.write('OCR improvements: We are aware that the accuracy of our OCR model could be improved.\
     As such, this could be done by training a model based on the user input compared to the original image.')
    st.write('Geolocalisation: If an item is made in Bangladesh for example and you are buying it in Portugal, it would not have the same \
    environmental impact as if you were buying it in Bangladesh. Therefore, integrating the added impact based on the location of \
    the buyer according to where the item was produced, could also be an interesting feature to add.')
    st.write('Business Opportunities: Perhaps a functionality could be integrated where the user is asked\
    for or what they are looking to buy (ie: party dress, pants etc.) and is recommended different sustainable \
    sources/shops, to buy such an item.')
