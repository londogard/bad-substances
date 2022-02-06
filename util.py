hormor_storande = [
    "Benzophenone-1",
    "Benzophenone-3",
    "BHA",
    "BHT",
    "Butylparaben",
    "Cyclomethicone",
    "Cyclotetrasiloxane",
    "Dimethylcyclosiloxane",
    "Ethylhexyl methoxycinnamate",
    "Propylparaben",
    "Resorcinol",
    "Triclosan",
    "Triphenyl Phosphate",
]
plast = [
    "Acrylate/Styrene copolymer",
    "Polyethylene",
    "Polymethyl methacrylate",
    "Polyethylene terephthalate",
    "Nylon",
]
maybe_cancer = [
    "Cyclotetrasiloxane",
    "PHMB",
    "Polyaminopropyl biguanide",
    "p-Aminophenol",
]
pfas = [
    "PTFE",
    "Polytef",
    "Polytefum",
    "benzyl",
    "C9-15 Fluoroalcohol phosphate",
    "C8-18 Fluoroalcohol phosphate",
    "Decafluoropentane",
    "Polyteym",
    "Perfluoroktansulfonat",
    "Perfluoroktansyra",
    "Ammonium C6-16 Perfluoroalkylethyl phosphate",
    "Polyperfluoroethoxymethoxy difluoroethyl PEG phosphate",
    "Polyperfluoromethylisopropyl ether",
    "Perfluorononyl dimethicone",
    "Dimetichonol Fluoralcohol dilinoleic acid",
    "Trifluoropropyl dimethicol",
    "Octafluoropentyl methacrylate",
]
pfas_include = ["perfluoro", "polyfluoro"]

bad_substances = set(
    [
        res.lower()
        for res in (hormor_storande + plast + maybe_cancer + pfas + pfas_include)
    ]
)
