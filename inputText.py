import streamlit as st
from util import get_bad_words
from util import print_bad_subtances

class InputText(object):
 
    def run(self):
        user_input = st.text_area("Insert the Table of Contents")
        user_input = user_input.split(",")

        user_input = [x.strip() for x in user_input]
        bad_substances_text = get_bad_words(user_input)
        print_bad_subtances(bad_substances_text)