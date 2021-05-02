hormor_storande = ['Benzophenone-1',
'Benzophenone-3',
'BHA',
'BHT',
'Butylparaben',
'Cyclomethicone',
'Cyclotetrasiloxane',
'Dimethylcyclosiloxane',
'Ethylhexyl methoxycinnamate',
'Propylparaben',
'Resorcinol',
'Triclosan',
'Triphenyl Phosphate']
plast = ['Acrylate/Styrene copolymer',
'Polyethylene',
'Polymethyl methacrylate',
'Polyethylene terephthalate',
'Nylon']
maybe_cancer = [
'Cyclotetrasiloxane',
'PHMB',
'Polyaminopropyl biguanide',
'p-Aminophenol',
]
pfas = [
'PTFE',
'Polytef',
'Polytefum',
'C9-15 Fluoroalcohol phosphate',
'C8-18 Fluoroalcohol phosphate',
'Decafluoropentane'
]
pfas_include = ['perfluoro']

import streamlit as st
import easyocr

def get_bad_words(substances):
    all_words = [res.lower() for res in (hormor_storande + plast + maybe_cancer + pfas + pfas_include)]
    ingredientes = [res.lower() for res in substances]
    print("substances", substances)
    print("Ingredients", ingredientes)
    bad_substances = []
    for ingredient in ingredientes:
        for x in [danger for danger in all_words if danger in ingredient]:
            bad_substances.append(x)
    return bad_substances

def print_bad_subtances(bad_substances):
    if bad_substances:
        st.text("Your table of contents include substances that are not recommended: ")
        for substance in bad_substances:
            st.text(substance)
    else:
        st.text("We can't find any substance that is not recommended.")

@st.cache(allow_output_mutation=True)
def getReader():
    return easyocr.Reader(['sv'], gpu = False)