from __future__ import annotations

import streamlit as st

from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from doctr.models.predictor import OCRPredictor
from doctr.utils.visualization import visualize_page

from numpy import ndarray

TWO_HOURS = 60 * 60 * 2


@st.experimental_memo(ttl=TWO_HOURS)
def read_files(img: bytes) -> list[ndarray]:
    return DocumentFile.from_images(img)


@st.experimental_memo(ttl=TWO_HOURS)
def get_predictor() -> OCRPredictor:
    return ocr_predictor(pretrained=True, assume_straight_pages=True)


@st.experimental_memo(ttl=TWO_HOURS)
def predict_texts(data: list[ndarray]):
    predictor = get_predictor()
    result = predictor(data)
    fig = visualize_page(result.pages[0].export(), data[0], interactive=False)
    st.pyplot(fig)
    # st.write(result.show(data))
    json_export = result.export()

    return json_export  # TODO draw this appealing.


def main():
    """Main function of the App"""
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
        data = read_files(img.getvalue())
        data = predict_texts(data)

        st.write(data)

        # text = [
        #    x[1] for x in data
        # ]  # TODO save and display bbox, in [0]. Score is in [2]
        # text = " ".join(text)
        # st.image(img, width=300)

    # if text:
    #    text = text.replace(",", " ").lower()
    #    text = text.split(" ")#
    # bad = set(text).intersection(bad_substances)
    # if len(bad):
    #    st.write(f"**Bad Substances Found:** {', '.join(bad)}")


if __name__ == "__main__":
    main()
    # TODO potentially look at symspellpy or something similar for close edits.
