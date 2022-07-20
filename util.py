from __future__ import annotations
import json
import streamlit as st

# reverse dict to retrieve risk/family/use..
# get set of data
@st.experimental_memo
def get_bad_substances() -> set[str]:
    with open("chemicals.json") as f:
        bad_substances_full = json.load(f)
    bad_substances = set()
    for family in bad_substances_full:
        substances = [x.lower() for x in family["substances"]]
        bad_substances.update(substances)

    return bad_substances
