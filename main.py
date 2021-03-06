from __future__ import annotations

import streamlit as st

from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from doctr.models.predictor import OCRPredictor
from doctr.utils.visualization import visualize_page

from numpy import ndarray
from symspellpy import SymSpell, Verbosity

from util import get_bad_substances, retrieve_best_guess

TWO_HOURS = 60 * 60 * 2


@st.experimental_memo(ttl=TWO_HOURS)
def read_files(img: bytes) -> list[ndarray]:
    return DocumentFile.from_images(img)


@st.experimental_memo
def get_predictor() -> OCRPredictor:
    return ocr_predictor(pretrained=True, assume_straight_pages=True)


@st.experimental_memo(ttl=TWO_HOURS)
def predict_texts(data: list[ndarray]):
    predictor = get_predictor()

    return predictor(data)  # TODO draw this appealing.


@st.experimental_memo(ttl=TWO_HOURS)
def visualize_result(result, _data):
    for i in range(len(result["pages"])):
        fig = visualize_page(result["pages"][i], _data[i], interactive=False)
    return fig


@st.experimental_memo
def get_symspell():
    symspell = SymSpell(max_dictionary_edit_distance=3, count_threshold=0)
    for word in get_bad_substances():
        symspell.create_dictionary_entry(word, 1)
    return symspell


def main():
    """Main function of the App"""
    st.header("Bad Substances - Find your enemies!")
    c1, c2 = st.columns(2)

    with c1:
        mode = st.radio("Select Mode", ["Image-file", "Text", "Camera"])
    img, text = None, None
    with c2:
        if mode == "Camera":
            img = st.camera_input("Camera Input!")
        elif mode == "Image-file":
            img = st.file_uploader("Input Image(s)")
        elif mode == "Text":
            text = st.text_area("Insert text")

    bad_substances = get_bad_substances()
    symspell = get_symspell()

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

        if len(words):
            c1, c2 = st.columns([1, 2])
            bad_list = "\n\n".join([str(w) for w in words])
            c1.write("### Bad Substances Found:")
            c1.write(bad_list)
            fig = visualize_result(result_json, imgs)
            c2.pyplot(fig)

        else:
            st.write("**No Bad Substances Found**")

    if text:
        text = text.replace(",", " ").lower()
        text = text.split(" ")
        bad = set(text).intersection(bad_substances)
        if len(bad):
            st.write(f"**Bad Substances Found:** {', '.join(bad)}")


if __name__ == "__main__":
    main()

    # TODO potentially look at symspellpy or something similar for close edits.
