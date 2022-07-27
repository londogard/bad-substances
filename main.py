from __future__ import annotations
from matplotlib.figure import Figure

import streamlit as st

from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from doctr.models.predictor import OCRPredictor
from doctr.utils.visualization import visualize_page

from numpy import ndarray

from util import prune_img_json, retrieve_best_guess, split_to_words
from util_symspell import get_symspell

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
def result_to_fig(result, _data) -> Figure:
    return visualize_page(result, _data, interactive=False)


@st.experimental_memo(ttl=TWO_HOURS)
def img_to_text_box_json(img: bytes) -> tuple[dict, list[str], ndarray]:
    imgs = read_files(img.getvalue())
    data = predict_texts(imgs)
    result = data.export()
    result = result["pages"][0]

    words = []
    for block in result["blocks"]:
        for line in block["lines"]:
            words += [word["value"].lower() for word in line["words"]]

    return result, words, imgs[0]


def sponsor_section():
    c1, c2 = st.columns(2)
    c1.markdown(
        """<a href="https://www.buymeacoffee.com/hlondogard" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 35px;" ></a>""",
        unsafe_allow_html=True,
    )
    c2.markdown(
        """<div style="display: flex; align-items: center;"><iframe src="https://github.com/sponsors/Lundez/button" title="Sponsor Lundez" height="35" width="116" style="border: 0;"></iframe><div>&nbsp;on GitHub</div></div>""",
        unsafe_allow_html=True,
    )


def main():
    """Main function of the App"""
    img, words = None, None

    sponsor_section()
    st.header("Bad Substances - Find your enemies!")
    c1, c2 = st.columns(2)
    with c1:
        mode = st.radio("Select Mode", ["Image-file", "Text", "Camera"])
    with c2:
        if mode == "Camera":
            img = st.camera_input("Camera Input!")
        elif mode == "Image-file":
            img = st.file_uploader(
                "Input Image",
                type=[
                    "jpg",
                    "png",
                    "jpeg",
                ],
            )
        elif mode == "Text":
            text = st.text_area("Insert text")
            words = split_to_words(text)

    if img is not None:
        img_json, words, img_ndarray = img_to_text_box_json(img)
    elif words is None:
        return st.warning("Add Input Data")

    symspell = get_symspell()
    words = [retrieve_best_guess(w, symspell) for w in words]
    words = [w for w in words if w is not None]

    if len(words):
        c1, c2 = st.columns([1, 2])
        bad_list = "\n\n".join([str(w) for w in words])
        c1.write("### Bad Substances Found:")
        c1.write(bad_list)

        if img is not None:
            img_json = prune_img_json(img_json, set([w.word for w in words]))
            fig = result_to_fig(img_json, img_ndarray)
            c2.pyplot(fig)
    else:
        st.write("**No Bad Substances Found**")


if __name__ == "__main__":
    main()
