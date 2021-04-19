try:
 
    from enum import Enum
    from io import BytesIO, StringIO
    from typing import Union
    from webcam import webcam
 
    import pandas as pd
    import streamlit as st
    import easyocr
    import cv2
    import numpy as np
    
except Exception as e:
    print(e)

STYLE = """
<style>
img {
    max-width: 100%;
}
</style>
"""

@st.cache(allow_output_mutation=True)
def getReader():
    return easyocr.Reader(['sv'], gpu = False)
 
hormor_storande = ['Benzophenone-1',
'Benzophenone-3',
'BHA',
'BHT',
'Butylparaben',
'Cyclomethicone',
'Cyclotetrasiloxane',
'Dimethylcyclosiloxane',
'Ethylhexyl methoxycinnamate',
'Propylparaben',
'Resorcinol',
'Triclosan',
'Triphenyl Phosphate']
plast = ['Acrylate/Styrene copolymer',
'Polyethylene',
'Polymethyl methacrylate',
'Polyethylene terephthalate',
'Nylon']
maybe_cancer = [
'Cyclotetrasiloxane',
'PHMB',
'Polyaminopropyl biguanide',
'p-Aminophenol',
]
pfas = [
'PTFE',
'Polytef',
'Polytefum',
'C9-15 Fluoroalcohol phosphate',
'C8-18 Fluoroalcohol phosphate',
'Decafluoropentane'
]
pfas_include = ['perfluoro']
 
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
 


def get_bad_words(substances):
    all_words = [res.lower() for res in (hormor_storande + plast + maybe_cancer + pfas + pfas_include)]
    ingredientes = [res.lower() for res in substances]
    print("substances", substances)
    print("Ingredients", ingredientes)
    bad_substances = []
    for ingredient in ingredientes:
        for x in [danger for danger in all_words if danger in ingredient]:
            bad_substances.append(x)
    return bad_substances

def print_bad_subtances(bad_substances):
    if bad_substances:
        st.text("Your table of contents include substances that are not recommended: ")
        for substance in bad_substances:
            st.text(substance)
    else:
        st.text("We can't find any substance that is not recommended.")

if __name__ ==  "__main__":
    reader = getReader()
    helper = FileUpload()
    helper.run()
