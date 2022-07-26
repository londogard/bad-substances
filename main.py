from __future__ import annotations
from matplotlib.figure import Figure

import streamlit as st

from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from doctr.models.predictor import OCRPredictor
from doctr.utils.visualization import visualize_page

from numpy import ndarray

from util import retrieve_best_guess, split_to_words

TWO_HOURS = 60 * 60 * 2


def read_files(img: bytes) -> list[ndarray]:
    return DocumentFile.from_images(img)


@st.experimental_memo
def get_predictor() -> OCRPredictor:
    return ocr_predictor(pretrained=True, assume_straight_pages=True)

def predict_texts(data: list[ndarray]):
    predictor = get_predictor()

    return predictor(data)


@st.experimental_memo(ttl=TWO_HOURS)
def result_to_fig(result, _data) -> Figure | None:
    if len(result["pages"]):
        result = result["pages"][0]
        return visualize_page(result, _data[0], interactive=False)

    return None

@st.experimental_memo(ttl=TWO_HOURS)
def img_to_text_box_json(img: bytes) -> dict:
        imgs = read_files(img.getvalue())
        data = predict_texts(imgs)
        result = data.export()

        for i in range(len(data.pages)):
            for block in result_json["pages"][i]["blocks"]:
                for line in block["lines"]:  # Dropping confidence etc..
                    potential_words = [
                        retrieve_best_guess(word["value"].lower(), symspell)
                        for word in line["words"]
                    ]
                    words += [x for x in potential_words if x is not None]
                    kept_words = set([x.word for x in potential_words if x is not None])
                    line["words"] = [
                        word
                        for word in line["words"]
                        if word["value"].lower() in kept_words
                    ]
        return 


def main():
    """Main function of the App"""
    img, text = None, None

    st.header("Bad Substances - Find your enemies!")
    c1, c2 = st.columns(2)

    with c1:
        mode = st.radio("Select Mode", ["Image-file", "Text", "Camera"])
    with c2:
        if mode == "Camera":
            img = st.camera_input("Camera Input!")
            img_json = img_to_text_box_json(img)
        elif mode == "Image-file":
            img = st.file_uploader("Input Image", type=["jpg", "png", "jpeg", ])
            img_json = img_to_text_box_json(img)
        elif mode == "Text":
            text = st.text_area("Insert text")
            words = split_to_words(text)

    if img is not None:

        pass
    elif text is not None:
        pass
    else:
        st.warning("Add Input Data")

    if img is not None:
        imgs = read_files(img.getvalue())
        data = predict_texts(imgs)
        result_json = data.export()

        words = []
        for i in range(len(data.pages)):
            for block in result_json["pages"][i]["blocks"]:
                for line in block["lines"]:  # Dropping confidence etc..
                    potential_words = [
                        retrieve_best_guess(word["value"].lower(), symspell)
                        for word in line["words"]
                    ]
                    words += [x for x in potential_words if x is not None]
                    kept_words = set([x.word for x in potential_words if x is not None])
                    line["words"] = [
                        word
                        for word in line["words"]
                        if word["value"].lower() in kept_words
                    ]

        if text:  # TODO fix
            words = text.replace(",", " ").lower()
            words = text.split(" ")

        if len(words):
            c1, c2 = st.columns([1, 2])
            bad_list = "\n\n".join([str(w) for w in words])
            c1.write("### Bad Substances Found:")
            c1.write(bad_list)
            
            fig = result_to_fig(result_json, imgs)
            if fig is not None:
                c2.pyplot(fig)
        else:
            st.write("**No Bad Substances Found**")


if __name__ == "__main__":
    main()
