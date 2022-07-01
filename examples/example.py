import numpy as np
import pandas as pd
import tmap as tm
from faerun import Faerun, FaerunPlot
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors as Descriptors
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
    with open("drugbank.smi") as f:
        for line in f.readlines():
            drugbank.append(line.split()[0].strip())

    mqns, smiles = get_fingerprint(drugbank)
    mqns = np.array(mqns)

    pca = PCA(n_components=3)
    result = pca.fit_transform(mqns)
    return result, mqns, smiles


def load_tmap():
    drugbank = []
    with open("drugbank.smi") as f:
        for line in f.readlines():
            drugbank.append(line.split()[0].strip())

    mqns, smiles = get_fingerprint(drugbank)
    mqns = np.array(mqns)

    return tm.embed(mqns)


coords, mqns, smiles = load()
smiles = [s + "__This is a Test" for s in smiles]

data = {"x": [], "y": [], "z": [], "c": [], "labels": smiles}

for i, e in enumerate(coords):
    data["x"].append(coords[i][0])
    data["y"].append(coords[i][1])
    data["z"].append(coords[i][2])
    data["c"].append(mqns[i][0])

df = pd.DataFrame.from_dict(data)

# plot = FaerunPlot()
# plot.add_series(x=df.x, y=df.y, z=df.z, c=df.c, labels=df.labels)
# plot.save("test", "smiles")

te = load_tmap()

plot = FaerunPlot(view="front")
plot.add_tmap_series(te, c=df.c)
plot.save("test", "smiles")
