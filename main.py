from enum import Enum
from io import BytesIO, StringIO
from typing import Union
from webcam import webcam

import pandas as pd
import streamlit as st
import easyocr
import numpy as np
from util import get_bad_words
from util import print_bad_subtances
from util import getReader
from inputText import InputText
from photo import Photo
from camera import Camera
 
st.markdown(
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">',
    unsafe_allow_html=True,
)
#query_params = st.experimental_get_query_params()
tabs = ["Input Text", "Camera", "Photo"]
active_tab =""
if not active_tab:
    active_tab = "Input Text"

if active_tab not in tabs:
    st.experimental_set_query_params(tab="Input Text")
    active_tab = "Input Text"

li_items = "".join(
    f"""
    <li class="nav-item">
        <a class="nav-link{' active' if t==active_tab else ''}" href="/?tab={t}">{t}</a>
    </li>
    """
    for t in tabs
)
tabs_html = f"""
    <ul class="nav nav-tabs">
    {li_items}
    </ul>
"""

st.markdown(tabs_html, unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

if active_tab == "Input Text":
    helper = InputText()
    helper.run()
    
elif active_tab == "Camera":
    helper = Camera()
    helper.run()
elif active_tab == "Photo":
    helper = Photo()
    helper.run()
else:
    st.text("Something went wrong")
    
    




   
