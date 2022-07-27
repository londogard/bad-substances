from __future__ import annotations

import streamlit as st
from symspellpy import SymSpell, Verbosity

from util import get_bad_substances


@st.experimental_memo
def get_symspell():
    symspell = SymSpell(max_dictionary_edit_distance=3, count_threshold=0)
    for word in get_bad_substances():
        symspell.create_dictionary_entry(word, 1)
    return symspell
