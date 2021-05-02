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
query_params = st.experimental_get_query_params()
tabs = ["Input Text", "Camera", "Photo"]
if "tab" in query_params:
    active_tab = query_params["tab"][0]
else:
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

class FileUpload(object):
 
    def __init__(self):
        self.fileTypes = ["csv", "png", "jpg"]
 
    def run(self):
        """
        Upload File on Streamlit Code
        :return:
        """
        st.info(__doc__)
        st.markdown(STYLE, unsafe_allow_html=True)
        file = st.file_uploader("Upload file", type=self.fileTypes)
        show_file = st.empty()
        user_input = st.text_area("Or add a text")
        captured_image = webcam()
        if not file and not user_input and not captured_image:
            show_file.info("Please upload a file of type: " + ", ".join(["csv", "png", "jpg"]))
            return
        #content = file.getvalue()
        if captured_image:
            st.write("Got an image from the webcam:")
            st.image(captured_image)
        if user_input:
            user_input = user_input.split(",")
            print("Hello", user_input)

            user_input = [x.strip() for x in user_input]
            bad_substances_text = get_bad_words(user_input)
            print_bad_subtances(bad_substances_text)
        if file and isinstance(file, BytesIO):
            try:
                fil = np.frombuffer(file.getbuffer(), np.uint8)
                substances = reader.readtext(file.read(), detail=0)
                bad_substances_image = get_bad_words(substances)
                print_bad_subtances(bad_substances)
            except Exception as e:
                st.text(e)
            
            show_file.image(file)
        #else:
            #data = pd.read_csv(file)
            #st.dataframe(data.head(10))
        #file.close()
 




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
    
    




   
