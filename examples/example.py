import numpy as np
import pandas as pd
from rdkit import RDLogger
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors as Descriptors
from faerun import Faerun
from sklearn.decomposition import PCA


def get_fingerprint(in_smiles):
    results = []
    smiles = []
    for s in in_smiles:
        mol = AllChem.MolFromSmiles(s)
        if mol is not None:
            if mol.GetNumAtoms() > 100:
                continue
            mqn = Descriptors.MQNs_(mol)
            results.append(np.array(mqn))
            smiles.append(s)

    return results, smiles


def load():
    drugbank = []
    with open('examples/drugbank.smi') as f:
        for line in f.readlines():
            drugbank.append(line.split()[0].strip())

    mqns, smiles = get_fingerprint(drugbank)
    mqns = np.array(mqns)

    pca = PCA(n_components=3)
    result = pca.fit_transform(mqns)
    return result, mqns, smiles

coords, mqns, smiles = load()

data = {
    'x': coords[:, 0],
    'y': coords[:, 1],
    'z': coords[:, 2],
    'c': 1.0 - mqns[:, 22] / max(mqns[22]),
    'smiles': smiles
}

df = pd.DataFrame.from_dict(data)


faerun = Faerun(view='free', shader='sphere')
faerun.plot(df, colormap='gist_rainbow')
