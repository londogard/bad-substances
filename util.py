from __future__ import annotations
from dataclasses import dataclass
import json
from typing import Any
import streamlit as st
from symspellpy import SymSpell, Verbosity


@dataclass
class Result:
    word: str
    info: SubstanceInfo
    distance: int

    def __str__(self) -> str:
        return f"{self.info}  \n(Original: _{self.word}_, Distance: {self.distance})"


@dataclass
class SubstanceInfo:
    term: str
    family: str
    info: str

    def __str__(self) -> str:
        info = f"\nInfo: _{self.info}_" if len(self.info) else ""
        return f"**{self.term}** ({self.family}):  {info}"


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


@st.experimental_memo
def get_substance_to_info() -> dict[str, SubstanceInfo]:
    with open("chemicals.json") as f:
        bad_substances_full = json.load(f)

    substance_to_info = dict()
    for family in bad_substances_full:
        for substance in family["substances"]:
            substance_to_info[substance.lower()] = SubstanceInfo(
                substance, family["family"], family.get("risks", "")
            )
    return substance_to_info


def retrieve_best_guess(word: str, symspell: SymSpell) -> Result | None:
    suggestion = symspell.lookup(word, Verbosity.TOP)

    if len(suggestion) and suggestion[0].distance < (len(word) / 2):
        return Result(
            word, get_substance_to_info()[suggestion[0].term], suggestion[0].distance
        )

    return None
