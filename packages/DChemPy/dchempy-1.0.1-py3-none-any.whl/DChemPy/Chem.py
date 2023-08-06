import rdkit
from rdkit import Chem


def NormalizeSmiles(smi):
    n_smi = Chem.MolToSmiles(Chem.MolFromSmiles(smi))
    print(n_smi)
    return n_smi

