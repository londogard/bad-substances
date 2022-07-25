from __future__ import annotations
import os

from numpy import ndarray

# Let's pick the desired backend
# os.environ['USE_TF'] = '1'
os.environ["USE_TORCH"] = "1"

import matplotlib.pyplot as plt

from doctr.io import DocumentFile
from doctr.models import ocr_predictor


def read_files(img: bytes) -> list[ndarray]:
    return DocumentFile.from_images(img)


def predict_texts(data: list[ndarray]):
    predictor = ocr_predictor(pretrained=True)
    result = predictor(data)
    result.show(data)
    # result.show(doc)
    json_export = result.export()

    return json_export  # TODO draw this appealing.
