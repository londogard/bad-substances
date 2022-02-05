import streamlit as st

import easyocr
from util import bad_substances


@st.cache
def get_easyocr():
    reader = easyocr.Reader(["en"])
    return reader


def main():
    """Main function of the App"""
    ocr = get_easyocr()

    st.header("Bad Substances - Find your enemies!")
    mode = st.radio("Select Mode", ["Image-file", "Text", "Camera"])
    img, text = None, None
    if mode == "Camera":
        img = st.camera_input("Camera Input!")
    elif mode == "Image-file":
        img = st.file_uploader("Input Image(s)")
    elif mode == "Text":
        text = st.text_area("Insert text")

    if img is not None:
        data = ocr.readtext(img.getvalue())
        text = [
            x[1] for x in data
        ]  # TODO save and display bbox, in [0]. Score is in [2]
        text = " ".join(text)
        st.image(img, width=300)

    if text:
        text = text.replace(",", " ").lower()
        text = text.split(" ")

        bad = set(text).intersection(bad_substances)
        if len(bad):
            st.write(f"**Bad Substances Found:** {', '.join(bad)}")


if __name__ == "__main__":
    main()
    # TODO potentially look at symspellpy or something similar for close edits.
