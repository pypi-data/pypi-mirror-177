"""
Modify SMILES String

Contents:
    DChemPy.Chem.NormalizeSmiles: Change SMILES into RDKit's standard format.
    DChemPy.Chem.NormalizeSmilesList: Change SMILES List into RDKit's standard format.
"""

import numpy as np
from rdkit import Chem


def NormalizeSmiles(smi):
    """
    Change SMILES into RDKit's standard format.

    :param smi: SMILES String
    :return: SMILES String with RDKit's standard format
    """
    n_smi = Chem.MolToSmiles(Chem.MolFromSmiles(smi))
    print(n_smi)
    return n_smi


def NormalizeSmilesList(smi_list):
    """
    Change SMILES List into RDKit's standard format.

    :param smi_list: List of SMILES String

    :return: List of SMILES String with RDKit's standard format
    """
    if type(smi_list) is np.ndarray:
        smi_list = list(smi_list.flatten())
    smi_out = []
    for smi in smi_list:
        n_smi = Chem.MolToSmiles(Chem.MolFromSmiles(smi))
        smi_out.append(n_smi)
    return smi_out
