from __future__ import annotations
import json


# reverse dict to retrieve risk/family/use..
# get set of data
def get_bad_substances() -> set[str]:
    bad_substances_full = json.load("chemicals.json")
    bad_substances = set()
    for family in bad_substances_full:
        substances = [x.lower() for x in family["substances"]]
        bad_substances.update(substances)

    return bad_substances
