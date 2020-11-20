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

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

from eco_fashion_project.data import get_data, preprocessing_image, get_fibre_list,\
get_nylon_group, get_polyester_group,get_linen_group,get_hemp_group,get_cotton_group,\
get_wool_group,get_viscose_group,get_leather_group, get_multi_fb_group_list, get_rest_group

from eco_fashion_project.trainer import ocr_core, split_lines, get_matches, get_fiber_pct, get_pct

st.title("Sustainahalic")

st.write("Please upload your tag")

st.write(pd.DataFrame{""})
st.DataFrame({tag_})
