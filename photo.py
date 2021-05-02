import streamlit as st
from util import get_bad_words
from util import print_bad_subtances
from io import BytesIO, StringIO
import numpy as np

STYLE = """
<style>
img {
    max-width: 100%;
}
</style>
"""

class Photo(object):
 
    def __init__(self):
        self.fileTypes = ["csv", "png", "jpg"]
 
    def run(self):
        st.info(__doc__)
        st.markdown(STYLE, unsafe_allow_html=True)
        file = st.file_uploader("Upload file", type=self.fileTypes)
        show_file = st.empty()
        if not file:
            show_file.info("Please upload a file of type: " + ", ".join(["csv", "png", "jpg"]))
            return
        if file and isinstance(file, BytesIO):
            try:
                fil = np.frombuffer(file.getbuffer(), np.uint8)
                substances = getReader().readtext(file.read(), detail=0)
                bad_substances_image = get_bad_words(substances)
                print_bad_subtances(bad_substances)
            except Exception as e:
                st.text(e)
            
            show_file.image(file)
        #else:
            #data = pd.read_csv(file)
            #st.dataframe(data.head(10))
        #file.close()