import streamlit as st
from util import get_bad_words
from util import print_bad_subtances
from io import BytesIO, StringIO
import numpy as np
from webcam import webcam

STYLE = """
<style>
img {
    max-width: 100%;
}
</style>
"""

class Camera(object):
 
    def write(self):
        captured_image = webcam()

        if captured_image and isinstance(captured_image, BytesIO):
            try:
                fil = np.frombuffer(file.getbuffer(), np.uint8)
                substances = getReader().readtext(file.read(), detail=0)
                bad_substances_image = get_bad_words(substances)
                print_bad_subtances(bad_substances)
            except Exception as e:
                st.text(e)