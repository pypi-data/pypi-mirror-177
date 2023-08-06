"""
Make SMILES into Feature Matrix and generate a full dataset.

Featurizor:
    DChemPy.Featurization.MFFFeat: MFF Featurizor
    DChemPy.Featurization.MFFFeatWithFrags: MFF Featurizor with specific fragments
    DChemPy.Featurization.RDKitDescFeat: RDKit Descriptor Featurizor
    DChemPy.Featurization.RDKitDescFeatWithName: RDKit Descriptor Featurizor with specific feature name
    DChemPy.Featurization.ConjuMolFeat: Conjugation descriptor Featurizor
    DChemPy.Featurization.NormMolFeat: 'Conjugation descriptor' Featurizor for the whole molecule, not only conju-stru
    DChemPy.Featurization.PeptideFeat: Peptide's amino sequence index featurizor

Tools:
    DChemPy.Featurization.PeptideToSmi: Turn list(peptide) into list(SMILES)
    DChemPy.Featurization.CombineX: Combine a series of X matrix
    DChemPy.Featurization.CombineTitle: Combine a series of title
    DChemPy.Featurization.CheckDataset: Check datasets: delete rows with nan&inf; delete columns whose maximum==minimum
    DChemPy.Featurization.MakeSaveY: Save y, ln(y), y/MolWt and ln(y/MolWt)
    DChemPy.Featurization.SaveXSmiTitle: Save X, title and smiles

Example:
    from DChemPy.Featurization import *
    X_mff, title_mff = MFFFeat(smiles_list, radius=3)
    X_rdkit , title_rdkit = RDKitDescFeat(smiles_list)
    X_conju, title_conju = ConjuMolFeat(smiles_list, title_mff)
    X = CombineX([X_mff, X_rdkit, X_conju])
    title = CombineTitle([title_mff, title_rdkit, title_conju])
    X_out, y_out, title_out, smiles_out = CheckDataset(X, y, title, smiles_list)
    MakeSaveY(y_out, value_ln=True, directory='data_out', note='_True')
    DChemPy.Featurization.SaveXSmiTitle(X_out, smiles_out, title_out, directory='data_out')
"""


from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors
from rdkit import DataStructs
from rdkit.Chem.EState.EState import EStateIndices
import numpy as np
import gc
import os
from pathlib import Path


def MFFFeat(smiles_rd, radius=2, addHatom=False, reserve_rate=0.05, exact_piece_reserve=False, exact_piece_smi=None,
            exact_piece_reserve_rate=0.0, turn_bool=False, turn_bool_mode='a', atom_count_control=True,
            min_frag_length=2, max_frag_length=50, omit_atom_count_control_frag_list=None, similarity_cal=False,
            similarity_method='Tanimoto', similarity_mode='mean'):
    """
    Generate MFF feature matrix.

    :param smiles_rd: List of SMILES string
    :param radius: ECFP Radius, default as '2'
    :param addHatom: Whether to add H in Mol, default as 'False'
    :param reserve_rate: Threshold of keeping a fragment column, default as '0.05'
    :param exact_piece_reserve: Whether to ignore 'reserve_rate' and keep fragments with specific smaller fragments,
                                default as 'False'
    :param exact_piece_smi: List of fragments to keep, default as 'None'
    :param exact_piece_reserve_rate:  Keep threshold of 'exact_piece_smi', default as '0.0'
    :param turn_bool: Whether to turn all MFF features into boolean form, default as 'False'
    :param turn_bool_mode: Mode of 'turn_bool', default as 'a', also can use 'b'
    :param atom_count_control: Whether to use atom-num control on fragments, default as 'True'
    :param min_frag_length: Minimum size of fragments, default as '2'
    :param max_frag_length: Maximum size of fragments, default as '50'
    :param omit_atom_count_control_frag_list: List of fragments to ignore 'atom_count_control', default as 'None'
    :param similarity_cal: Whether to calculate similarity with all other fragments for MFF values of 0,
                           default as 'False'
    :param similarity_method: Mode of similarity calculation, default as 'Tanimoto', also can use 'MACCS'
    :param similarity_mode: Calculate method of similarity calculation, default as 'mean', also can use 'max'

    :return: A tuple of (X, title)
             X: numpy array with shape of (len(smiles_rd), num_of_frags)
             title: numpy array with shape of (num_of_frags, 1)

    example:
    X_mff, title_mff = DChemPy.Featurization.MFFFeat(smiles_list)
    X_mff, title_mff = DChemPy.Featurization.MFFFeat(smiles_list, radius=3)
    """
    if type(smiles_rd) is np.ndarray:
        smiles_rd = smiles_rd.flatten().tolist()
    frag_smiles_list = []
    mol_list_temp = []
    for _ in range(len(smiles_rd)):
        smi = smiles_rd[_]
        mol = Chem.MolFromSmiles(smi)
        if addHatom:
            mol = Chem.AddHs(mol)
        mol_list_temp.append(mol)
        info = {}
        fp = rdMolDescriptors.GetMorganFingerprint(mol, radius, useChirality=True, useBondTypes=True, useFeatures=True,
                                                   bitInfo=info)
        fp = fp.GetNonzeroElements()
        for fragment_id, count in fp.items():
            root, radius = info[fragment_id][0]
            env = Chem.FindAtomEnvironmentOfRadiusN(mol, radius, root)
            frag = Chem.PathToSubmol(mol, env)
            f_smiles = Chem.MolToSmiles(frag)
            if f_smiles != '':
                frag_smiles_list.append(f_smiles)
    print('Number of all original fragments:', len(frag_smiles_list))
    title = np.unique(frag_smiles_list)
    data = np.zeros((len(smiles_rd), len(title)))
    for i in range(len(smiles_rd)):
        m = mol_list_temp[i]
        for j in range(len(title)):
            f = title[j]
            patt = Chem.MolFromSmarts(f)
            atomids = m.GetSubstructMatches(patt)
            data[i, j] = len(atomids)
    print('Before delete sparse columns: shape of data:', data.shape)
    del mol_list_temp
    gc.collect()
    # Delete less filled fragments:
    delete = []
    for i in range(data.shape[1]):
        filled_rate = sum(data[:, i] != 0) / data.shape[0]
        if filled_rate < reserve_rate:
            if exact_piece_reserve:
                if exact_piece_smi is None:
                    exact_piece_smi = []
                m = Chem.MolFromSmarts(title[i])
                for patt_temp in exact_piece_smi:
                    patt = Chem.MolFromSmarts(patt_temp)
                    flag = m.HasSubstructMatch(patt)
                    if flag:
                        break
                if filled_rate >= exact_piece_reserve_rate:
                    continue
            delete.append(i)
    data = np.delete(data, delete, axis=1)
    title = np.array(title).reshape(1, len(title))
    title = np.delete(title, delete, axis=1)
    title = list(title.flatten())
    print('After delete sparse columns: shape of data:', data.shape)
    if atom_count_control:
        if omit_atom_count_control_frag_list is None:
            omit_atom_count_control_frag_list = []
        delete = []
        for i in range(data.shape[1]):
            flag = False
            m = Chem.MolFromSmarts(title[i])
            for patt_temp in omit_atom_count_control_frag_list:
                patt = Chem.MolFromSmarts(patt_temp)
                flag = m.HasSubstructMatch(patt)
                if flag:
                    break
            if flag:
                continue
            atom_count = len(m.GetAtoms())
            if atom_count < min_frag_length or atom_count > max_frag_length:
                delete.append(i)
        data = np.delete(data, delete, axis=1)
        title = np.array(title).reshape(1, len(title))
        title = np.delete(title, delete, axis=1)
        title = list(title.flatten())
        print('After atom-count control: shape of data:', data.shape)
    if turn_bool:
        bool_patt_list = title
        for bool_patt in bool_patt_list:
            index_t = title.index(bool_patt)
            feature_max = int(max(data[:, index_t]))
            # 制作新的bool数据数组
            if turn_bool_mode == 'a':
                matrix_bool = np.zeros((data.shape[0], feature_max))
            else:
                matrix_bool = np.zeros((data.shape[0], feature_max + 1))
            for i in range(data.shape[0]):
                if turn_bool_mode == 'a':
                    if data[i, index_t] >= 1:
                        matrix_bool[i, int(data[i, index_t] - 1)] = 1
                else:
                    matrix_bool[i, int(data[i, index_t])] = 1
            data = np.delete(data, [index_t], axis=1)
            title = np.array(title).reshape(1, len(title))
            title = np.delete(title, [index_t], axis=1)
            title = list(title.flatten())
            new_title = []
            if turn_bool_mode == 'a':
                for i in range(feature_max):
                    new_title.append('With_' + str(i + 1) + '_' + bool_patt)
            else:
                for i in range(feature_max + 1):
                    new_title.append('With_' + str(i) + '_' + bool_patt)
            data = np.hstack((data, matrix_bool))
            title = [*title, *new_title]
        delete = []
        for i in range(data.shape[1]):
            if sum(data[:, i]) == 0:
                delete.append(i)
        data = np.delete(data, delete, axis=1)
        title = np.array(title).reshape(1, len(title))
        title = np.delete(title, delete, axis=1)
        title = list(title.flatten())
        print('title length(after turn to bool):', len(title))
        print('data shape(after turn to bool):', data.shape, '\n')
    if similarity_cal:
        data = data.astype(float)
        for i in range(data.shape[0]):
            emp = []
            emp_list = []
            fill = []
            fill_list = []
            for j in range(len(title)):
                if data[i, j] >= 1:
                    fill.append(title[j])
                    fill_list.append(j)
                elif data[i, j] == 0:
                    emp.append(title[j])
                    emp_list.append(j)
            for smi1_idx in emp_list:
                similarity = []
                smi1 = title[smi1_idx]
                fps1 = Chem.RDKFingerprint(Chem.MolFromSmarts(smi1))
                for smi2_idx in fill_list:
                    smi2 = title[smi2_idx]
                    fps2 = Chem.RDKFingerprint(Chem.MolFromSmarts(smi2))
                    sm = 0
                    if similarity_method == 'Tanimoto':
                        sm = DataStructs.FingerprintSimilarity(fps1, fps2)
                    elif similarity_method == 'MACCS':
                        sm = DataStructs.FingerprintSimilarity(fps1, fps2, metric=DataStructs.DiceSimilarity)
                    sm *= data[i, smi2_idx]
                    similarity.append(sm)
                sim = 0
                if similarity_mode == 'max':
                    sim = np.max(similarity)
                elif similarity_mode == 'mean':
                    sim = np.mean(similarity)
                data[i, smi1_idx] += sim
    x = data
    title = np.array(title).reshape(x.shape[1], 1)
    return x, title


def MFFFeatWithFrags(smiles_rd, frag_list):
    """
    Generate MFF feature matrix with given fragments.

    :param smiles_rd: List of SMILES string of molecules
    :param frag_list: List of SMILES string of fragments

    :return: A tuple of (X, title)
             X: numpy array with shape of (len(smiles_rd), num_of_frags)
             title: numpy array with shape of (num_of_frags, 1)

    example:
    X_mff, temp = DChemPy.Featurization.MFFFeatWithFrags(smiles_list, frag_list)
    """
    if type(smiles_rd) is np.ndarray:
        smiles_rd = list(smiles_rd.flatten())
    if type(frag_list) is np.ndarray:
        frag_list = list(frag_list.flatten())
    x = np.zeros((len(smiles_rd), len(frag_list)))
    for i in range(len(smiles_rd)):
        smi = smiles_rd[i]
        mol = Chem.MolFromSmiles(smi)
        for j in range(len(frag_list)):
            f = frag_list[j]
            patt = Chem.MolFromSmarts(f)
            atomids = mol.GetSubstructMatches(patt)
            x[i, j] = len(atomids)
    title = np.array(frag_list).reshape(x.shape[1], 1)
    return x, title


def RDKitDescFeat(smiles_rd):
    """
    Generate RDKit feature matrix

    :param smiles_rd: List of SMILES string of molecules

    :return: A tuple of (X, title)
             X: numpy array with shape of (len(smiles_rd), num_of_features)
             title: numpy array with shape of (num_of_features, 1)

    example:
    X_rdkit, title_rdkit = DChemPy.Featurization.RDKitDescFeat(smiles_list)
    """
    allowed = ['NOCount', 'VSA_EState4', 'NumHDonors', 'SlogP_VSA12', 'NumRadicalElectrons', 'SlogP_VSA4',
                          'Kappa2', 'Chi2n', 'PEOE_VSA3', 'PEOE_VSA7', 'PEOE_VSA4', 'Chi1', 'MolWt', 'SMR_VSA1',
                          'SlogP_VSA9', 'VSA_EState9', 'MaxAbsPartialCharge', 'NumSaturatedHeterocycles',
                          'MaxPartialCharge', 'VSA_EState1', 'PEOE_VSA6', 'EState_VSA11', 'SMR_VSA4', 'EState_VSA7',
                          'VSA_EState2', 'NHOHCount', 'SlogP_VSA10', 'SMR_VSA7', 'PEOE_VSA9', 'NumAliphaticRings',
                          'EState_VSA8', 'PEOE_VSA5', 'BertzCT', 'SlogP_VSA1', 'SlogP_VSA6', 'PEOE_VSA1', 'VSA_EState7',
                          'MinAbsPartialCharge', 'LabuteASA', 'SlogP_VSA2', 'EState_VSA4', 'MolMR', 'Kappa1',
                          'NumHAcceptors', 'EState_VSA9', 'MolLogP', 'NumAromaticHeterocycles', 'BalabanJ',
                          'FractionCSP3', 'SMR_VSA3', 'RingCount', 'NumSaturatedRings', 'PEOE_VSA2',
                          'MaxAbsEStateIndex', 'Kappa3', 'Chi3n', 'NumRotatableBonds', 'Chi4n', 'VSA_EState3',
                          'SMR_VSA8', 'MinPartialCharge', 'EState_VSA6', 'SMR_VSA9', 'PEOE_VSA13',
                          'NumValenceElectrons', 'MaxEStateIndex', 'SMR_VSA6', 'VSA_EState8', 'EState_VSA2',
                          'NumAromaticCarbocycles', 'SMR_VSA10', 'SlogP_VSA3', 'HallKierAlpha', 'PEOE_VSA14',
                          'HeavyAtomCount', 'VSA_EState10', 'SlogP_VSA11', 'ExactMolWt', 'MinAbsEStateIndex', 'TPSA',
                          'PEOE_VSA10', 'SMR_VSA2', 'Chi1v', 'Chi4v', 'PEOE_VSA8', 'EState_VSA5', 'Chi1n',
                          'VSA_EState5', 'SlogP_VSA7', 'HeavyAtomMolWt', 'MinEStateIndex', 'NumAliphaticHeterocycles',
                          'VSA_EState6', 'Chi0v', 'SlogP_VSA5', 'SMR_VSA5', 'Chi0', 'Chi2v', 'NumSaturatedCarbocycles',
                          'NumAromaticRings', 'Chi0n', 'PEOE_VSA12', 'Chi3v', 'NumAliphaticCarbocycles',
                          'EState_VSA10', 'EState_VSA3', 'EState_VSA1', 'NumHeteroatoms', 'SlogP_VSA8', 'PEOE_VSA11']
    if type(smiles_rd) is np.ndarray:
        smiles_rd = smiles_rd.flatten().tolist()
    descriptors = []
    desc_list = []
    for descriptor, function in Descriptors.descList:
        if descriptor in allowed:
            descriptors.append(descriptor)
            desc_list.append((descriptor, function))
    title = np.array(descriptors).reshape(len(descriptors), 1)
    data = []
    for i in range(len(smiles_rd)):
        mol = Chem.MolFromSmiles(smiles_rd[i])
        res = []
        for desc_name, f in desc_list:
            res.append(f(mol))
        data.append(res)
    data = np.array(data)
    print('RDKit Desc Data Shape:', data.shape)
    x = data
    return x, title


def RDKitDescFeatWithName(smiles_rd, desc_name_list):
    """
    Generate RDKit feature matrix with specific feature name

    :param smiles_rd: List of SMILES string of molecules
    :param desc_name_list: List of descriptor name of RDKit descriptors

    :return: A tuple of (X, title)
             X: numpy array with shape of (len(smiles_rd), num_of_features)
             title: numpy array with shape of (num_of_features, 1)

    example:
    X_rdkit, title_rdkit = DChemPy.Featurization.RDKitDescFeatWithName(smiles_list, desc_name_list)
    """
    if type(smiles_rd) is np.ndarray:
        smiles_rd = smiles_rd.flatten().tolist()
    descriptors = []
    desc_list = []
    for descriptor, function in Descriptors.descList:
        if descriptor in desc_name_list:
            descriptors.append(descriptor)
            desc_list.append((descriptor, function))
    title = np.array(descriptors).reshape(len(descriptors), 1)
    data = []
    for i in range(len(smiles_rd)):
        mol = Chem.MolFromSmiles(smiles_rd[i])
        res = []
        for desc_name, f in desc_list:
            res.append(f(mol))
        data.append(res)
    data = np.array(data)
    print('RDKit Desc Data Shape:', data.shape)
    x = data
    return x, title


def ConjuMolFeat(smiles_rd, mff_title_list=None, keep_type='max'):
    """
    Generate Conjugation descriptor matrix

    :param smiles_rd: List of SMILES string of molecules
    :param keep_type: Mode of calculation for MOE-like descriptors, default as 'max', also can use 'mean' or 'acc-mean'
    :param mff_title_list: List of MFF titles, needed for calculation, default as None

    :return: A tuple of (X, title)
             X: numpy array with shape of (len(smiles_rd), num_of_features)
             title: numpy array with shape of (num_of_features, 1)

    example:
    X_conju, title_conju = DChemPy.Featurization.ConjuMolFeat(smiles_list, mff_title_list=mff_title_list)
    """
    if type(smiles_rd) is np.ndarray:
        smiles_rd = list(smiles_rd.flatten())
    if type(mff_title_list) is np.ndarray:
        mff_title_list = list(mff_title_list.flatten())
    # For MOE-like VSA Descriptors:
    dij_m = np.zeros((54, 54))
    ri_m = np.zeros((54, 1))
    ri_m[6, 0] = 1.950  # C
    ri_m[7, 0] = 1.950  # N
    ri_m[8, 0] = 1.779  # O
    ri_m[9, 0] = 1.496  # F
    ri_m[15, 0] = 2.287  # P
    ri_m[16, 0] = 2.185  # S
    ri_m[17, 0] = 2.044  # Cl
    ri_m[35, 0] = 2.166  # Br
    ri_m[53, 0] = 2.358  # I
    dij_m[6, 35] = 1.970  # C-Br
    dij_m[35, 6] = 1.970
    dij_m[7, 35] = 1.840  # N-Br
    dij_m[35, 7] = 1.840
    dij_m[6, 6] = 1.540  # C-C
    dij_m[7, 7] = 1.450  # N-N
    dij_m[8, 8] = 1.470  # O-O
    dij_m[6, 17] = 1.800  # C-Cl
    dij_m[17, 6] = 1.800
    dij_m[6, 9] = 1.350  # C-F
    dij_m[9, 6] = 1.350
    dij_m[6, 53] = 2.120  # C-I
    dij_m[53, 6] = 2.120
    dij_m[6, 7] = 1.470  # C-N
    dij_m[7, 6] = 1.470
    dij_m[6, 8] = 1.430  # C-N
    dij_m[8, 6] = 1.430
    dij_m[6, 15] = 1.850  # C-P
    dij_m[15, 6] = 1.850
    dij_m[6, 16] = 1.810  # C-S
    dij_m[16, 6] = 1.810
    dij_m[7, 8] = 1.460  # N-O
    dij_m[8, 7] = 1.460
    dij_m[7, 15] = 1.600  # N-P
    dij_m[15, 7] = 1.600
    dij_m[7, 16] = 1.760  # N-S
    dij_m[16, 7] = 1.760
    dij_m[8, 15] = 1.570  # O-P
    dij_m[15, 8] = 1.570
    dij_m[8, 16] = 1.570  # O-S
    dij_m[16, 8] = 1.570

    def find_conju(mol, a_m):
        patt_list_d = ['C=C', 'C#C', 'C#N', 'C=O', 'C=S', 'C=N', 'N=N', '[N+]([O-])=O']
        patt_list_m = ['N', 'O', 'S', 'F', 'Cl', 'Br', 'I', 'P']
        ring_list = []
        f_a = []
        patt = Chem.MolFromSmarts('c')
        atomids = mol.GetSubstructMatches(patt)
        atoms = mol.GetAtoms()
        temp_list = []

        def find_ring(atom_id, found_atoms):
            nonlocal a_m, ring_list, f_a, atoms, temp_list
            c_flag = False
            c_list = np.argwhere(a_m[atom_id] == 1).flatten().tolist()
            for atom in c_list:
                if atom not in f_a:
                    a = atoms[atom]
                    if a.IsInRing() and str(a.GetHybridization()) != 'SP3':
                        found_atoms.append(atom)
                        f_a.append(atom)
                        find_ring(atom, found_atoms)
                        c_flag = True
            if not c_flag:
                temp_list.append(found_atoms)

        for atom in atomids:
            a = atom[0]
            if a not in f_a:
                find_ring(a, [])
            if len(temp_list) > 0:
                max_ring = temp_list[0]
                for l in temp_list:
                    if len(l) > len(max_ring):
                        max_ring = l
                ring_list.append(max_ring)
            temp_list = []
        for patt in patt_list_d:
            f = Chem.MolFromSmarts(patt)
            atomids = mol.GetSubstructMatches(f)
            if len(atomids) > 0:
                for pair in atomids:
                    n_l = []
                    flag_f = False
                    for a in pair:
                        if a in f_a:
                            flag_f = True
                            break
                        neighbors = atoms[a].GetNeighbors()
                        for na in neighbors:
                            n_l.append(na.GetIdx())
                    if flag_f:
                        continue
                    temp = []
                    temp_r_id = []
                    for n in n_l:
                        if atoms[n].GetAtomicNum() in [6, 7, 8]:
                            for i in range(len(ring_list)):
                                ring = ring_list[i]
                                if n in ring:
                                    temp.append(ring)
                                    temp_r_id.append(i)
                    if len(temp) == 1:
                        ring_list[temp_r_id[0]].append(pair[0])
                        ring_list[temp_r_id[0]].append(pair[1])
                        f_a.append(pair[0])
                        f_a.append(pair[1])
                    else:
                        t_r = []
                        for r in temp:
                            t_r += r
                        t_r.append(pair[0])
                        t_r.append(pair[1])
                        temp_r_id.sort()
                        temp_r_id = np.unique(temp_r_id)
                        for i in reversed(temp_r_id):
                            del ring_list[i]
                        ring_list.append(t_r)
                        f_a.append(pair[0])
                        f_a.append(pair[1])
        for patt in patt_list_m:
            f = Chem.MolFromSmarts(patt)
            atomids = mol.GetSubstructMatches(f)
            if len(atomids) > 0:
                for atom in atomids:
                    a = atom[0]
                    if a not in f_a:
                        neighbors = atoms[a].GetNeighbors()
                        n_l = []
                        for na in neighbors:
                            n_l.append(na.GetIdx())
                        temp = []
                        temp_r_id = []
                        for n in n_l:
                            for i in range(len(ring_list)):
                                ring = ring_list[i]
                                if (n in ring) and (i not in temp_r_id):
                                    temp.append(ring)
                                    temp_r_id.append(i)
                        if len(temp) == 1:
                            ring_list[temp_r_id[0]].append(a)
                            f_a.append(a)
                        else:
                            t_r = []
                            for r in temp:
                                t_r += r
                            t_r.append(a)
                            temp_r_id.sort()
                            for i in reversed(temp_r_id):
                                del ring_list[i]
                            if len(t_r) > 1:
                                ring_list.append(t_r)
                                f_a.append(a)
        for i in range(len(atoms)):
            if i not in f_a:
                aa = atoms[i]
                if aa.GetSymbol() != 'C' or str(aa.GetHybridization()) != 'SP2':
                    continue
                aa_n = aa.GetNeighbors()
                flag = False
                for aaa in aa_n:
                    if aaa.GetIdx() in f_a:
                        flag = True
                        break
                if flag:
                    a = i
                    neighbors = atoms[a].GetNeighbors()
                    n_l = []
                    for na in neighbors:
                        n_l.append(na.GetIdx())
                    temp = []
                    temp_r_id = []
                    for n in n_l:
                        for i in range(len(ring_list)):
                            ring = ring_list[i]
                            if (n in ring) and (i not in temp_r_id):
                                temp.append(ring)
                                temp_r_id.append(i)
                    if len(temp) == 1:
                        ring_list[temp_r_id[0]].append(a)
                        f_a.append(a)
                    else:
                        t_r = []
                        for r in temp:
                            t_r += r
                        t_r.append(a)
                        temp_r_id.sort()
                        for i in reversed(temp_r_id):
                            del ring_list[i]
                        if len(t_r) > 1:
                            ring_list.append(t_r)
                            f_a.append(a)
        if len(ring_list) > 1:
            flag = True
            while flag:
                t_temp = int(len(ring_list) * (len(ring_list) - 1) / 2)
                _temp = 0
                break_flag = False
                for i in range(len(ring_list) - 1):
                    for ji in range(len(ring_list) - i - 1):
                        r_1 = ring_list[i]
                        r_2 = ring_list[i + ji + 1]
                        if np.sum(a_m[r_1, :][:, r_2]) == 0:
                            _temp += 1
                        else:
                            for ki in r_2:
                                ring_list[i].append(ki)
                            ring_list[i] = np.unique(ring_list[i])
                            del ring_list[i + ji + 1]
                            break_flag = True
                            break
                    if break_flag:
                        break
                if _temp == t_temp:
                    flag = False
        for i in range(len(ring_list)):
            ring_list[i] = np.unique(ring_list[i]).flatten().tolist()
        return ring_list, f_a

    def find_elec_num(kind, _hyb):
        one_list = ['C']
        two_list = ['N', 'O', 'S', 'P', 'F', 'Cl', 'Br', 'I']
        if kind in one_list:
            return 1
        elif kind in two_list:
            if _hyb == 'SP' and kind in ['N', 'P', 'O']:
                return 1
            elif _hyb == 'SP2' and kind in ['N', 'O', 'S']:
                return 1
            else:
                return 2

    CONJU_TITLE = []
    CONJU_PRE = ['Apperant-Elec-Count', 'PEOE-Charge', 'EState-Indice', 'Atomic-LogP', 'Atomic-MR']
    CONJU_NUM = 5 + 7 + 16 * len(CONJU_PRE)
    data_conju = np.zeros((len(smiles_rd), CONJU_NUM))
    descList = []
    allowedDescriptors = ['MolWt']
    for descriptor, function in Descriptors.descList:
        if descriptor in allowedDescriptors:
            descList.append((descriptor, function))

    for _ in range(len(smiles_rd)):
        smi = smiles_rd[_]
        mol = Chem.MolFromSmiles(Chem.MolToSmiles(Chem.MolFromSmiles(smi)))
        atoms = mol.GetAtoms()
        a_m = Chem.rdmolops.GetAdjacencyMatrix(mol)
        d_m = Chem.rdmolops.GetDistanceMatrix(mol)
        res = find_conju(mol, a_m)
        ring_list = res[0]
        f_a = res[1]
        conju_size_list = [len(r) for r in ring_list]
        # Calculate apparent conjugation charges:
        app_elec = []
        for a in range(len(atoms)):
            if a in f_a:
                a_kind = atoms[a].GetSymbol()
                hyb = str(atoms[a].GetHybridization())
                app_elec.append(find_elec_num(a_kind, hyb))
            else:
                app_elec.append(0)
        # Calculate PEOE Charges:
        AllChem.ComputeGasteigerCharges(mol, nIter=25)
        peoe_charge = [mol.GetAtomWithIdx(i).GetDoubleProp('_GasteigerCharge') for i in range(mol.GetNumAtoms())]
        # Calculate EState Indices:
        estate_index = EStateIndices(mol)
        # Calculate atomic contribution of LogP and MR:
        contribs = rdMolDescriptors._CalcCrippenContribs(mol)
        logp = [contribs[i][0] for i in range(len(contribs))]
        mr = [contribs[i][1] for i in range(len(contribs))]

        atom_props = [app_elec, peoe_charge, estate_index, logp, mr]

        if _ == 0:
            CONJU_TITLE.append('Num of Conju-Stru (MFF-Conju)')  # 1.
            CONJU_TITLE.append('Num of Conju-All-Atoms (MFF-Conju)')  # 2.
            CONJU_TITLE.append('Atom Num Conju-All Ratio (MFF-Conju)')  # 3.
            CONJU_TITLE.append('AtomWt Conju-All Ratio (MFF-Conju)')  # 4.
            CONJU_TITLE.append('Full-Mol Wiener Index (MFF-Conju)')  # 5.
            CONJU_TITLE.append('Individual Conju-Atom Number (MFF-Conju)')  # 6.
            CONJU_TITLE.append('Conju-Part-Wt (MFF-Conju)')  # 7.
            CONJU_TITLE.append('Conju-AtomicWt (MFF-Conju)')  # 8.
            CONJU_TITLE.append('Max Conju-Distance (MFF-Conju)')  # 9.
            CONJU_TITLE.append('Conju-Branch Index (MFF-Conju)')  # 10.
            CONJU_TITLE.append('Conju-Stru Wiener Index (MFF-Conju)')  # 11.
            CONJU_TITLE.append('Conju-Stru-VSA (MFF-Conju)')  # 12.
        # 1. Number of conjugation structures:
        data_conju[_, 0] = len(ring_list)
        # 2. Total number of atoms in all conjugation structures:
        data_conju[_, 1] = len(f_a)
        # 3. Ratio of conjugated and non-conjugated atoms:
        data_conju[_, 2] = len(f_a) / len(atoms)
        # 4. Ratio of conjugated and non-conjugated fragment weights:
        rval = []
        for desc_name, function in descList:
            rval.append(function(mol))
        wt_list = []
        mwt_list = []
        for r in ring_list:
            tt = 0
            for a in r:
                tt += atoms[a].GetMass()
            wt_list.append(tt)
            mwt_list.append(tt / len(r))
        data_conju[_, 3] = sum(wt_list) / rval[0]
        # 5. Wiener Index:
        if '.' in smi:
            mol22 = Chem.MolFromSmiles(smi.split('.')[0])
            dm22 = Chem.rdmolops.GetDistanceMatrix(mol22)
            data_conju[_, 4] = np.sum(dm22) / (2 * dm22.shape[0] * (dm22.shape[0] - 1))
        else:
            data_conju[_, 4] = np.sum(d_m) / (2 * d_m.shape[0] * (d_m.shape[0] - 1))

        # Indenpent features of conjugation structures:
        conju_props = []
        # 6. Atom numbers of individual conjugation structures:
        size_l = []
        for r in ring_list:
            size_l.append(len(r))
        conju_props.append(size_l)
        # 7. Weights of individual conjugation structures:
        conju_props.append(wt_list)
        # 8. Mean atomic weights of individual conjugation structures:
        conju_props.append(mwt_list)
        # 9. Size of individual conjugation structures:
        conju_max_dis = []
        for r in ring_list:
            conju_max_dis.append(np.max(d_m[r, :][:, r]))
        conju_props.append(conju_max_dis)

        # 10. Branching index of individual conjugation structures:
        branch_l = []
        for i in range(len(wt_list)):
            branch_l.append(np.sum(a_m[ring_list[i], :][:, ring_list[i]]) / (2 * size_l[i]))
        conju_props.append(branch_l)

        # 11. Weiner index of individual conjugation structures:
        wi_l = []
        for r in ring_list:
            d_m_temp = d_m[r, :][:, r]
            wi_l.append(np.sum(d_m_temp) / (2 * d_m_temp.shape[0] * (d_m_temp.shape[0] - 1)))
        conju_props.append(wi_l)

        # 12. VSA of individual conjugation structures:
        conju_vsa_l = []
        for r in ring_list:
            vsa_t = 0
            for i in range(len(r)):
                vsa_tt = 0
                atom = atoms[r[i]]
                n_l = atom.GetNeighbors()
                aid_1 = atom.GetAtomicNum()
                ar_1 = ri_m[aid_1, 0]
                for j in range(len(n_l)):
                    aid_2 = n_l[j].GetAtomicNum()
                    ar_2 = ri_m[aid_2, 0]
                    dij_i = dij_m[aid_1, aid_2]
                    dij = min(max(abs(ar_1 - ar_2), dij_i), ar_1 + ar_2)
                    vsa_tt += (ar_2 ** 2 - (ar_1 - dij) ** 2) / dij
                vsa_t += 4 * np.pi * ar_1 ** 2 - np.pi * ar_1 * vsa_tt
            conju_vsa_l.append(vsa_t)
        conju_props.append(conju_vsa_l)

        # Atomic Descriptors:
        for __ in range(len(atom_props)):
            PRE = 'Conju-' + CONJU_PRE[__] + '-'
            END_P = ' (MFF-Conju)'
            atom_props_list = atom_props[__]
            if _ == 0:
                CONJU_TITLE.append(PRE + 'Sum' + END_P)  # 13.1.
                CONJU_TITLE.append(PRE + 'AtomicMean' + END_P)  # 13.2.
                CONJU_TITLE.append(PRE + 'Maximum' + END_P)  # 13.3.
                CONJU_TITLE.append(PRE + 'Minimum' + END_P)  # 13.4.
                CONJU_TITLE.append(PRE + 'Delta' + END_P)  # 13.5.
                CONJU_TITLE.append(PRE + 'Influence' + END_P)  # 13.6.
                CONJU_TITLE.append(PRE + 'AtomicInfluence' + END_P)  # 13.7.
                CONJU_TITLE.append(PRE + 'PositiveDisCoef' + END_P)  # 13.8.
                CONJU_TITLE.append(PRE + 'PairMean-PositiveDisCoef' + END_P)  # 13.9.
                CONJU_TITLE.append(PRE + 'NegativeDisCoef' + END_P)  # 13.10.
                CONJU_TITLE.append(PRE + 'PairMean-NegativeDisCoef' + END_P)  # 13.11.
                CONJU_TITLE.append(PRE + 'GradSum' + END_P)  # 13.12.
                CONJU_TITLE.append(PRE + 'PairMean-Grad' + END_P)  # 13.13.
                CONJU_TITLE.append(PRE + 'MaxMinDisRatio' + END_P)  # 13.14.
                # CONJU_TITLE.append(PRE+'AppearantU'+END_P)  # 13.15.
                CONJU_TITLE.append(PRE + 'LaplaceSum' + END_P)  # 13.16.
                CONJU_TITLE.append(PRE + 'PairMean-Laplace' + END_P)  # 13.17.
            # 13.1. Sum without fragment:
            x_count_l = []
            # 13.2. Atomic mean without fragments:
            x_atom_mean_l = []
            # 13.3. Maximum with fragments:
            x_max_l = []
            # 13.4. Minimum with fragments:
            x_min_l = []
            # 13.5. Max-Min with fragments:
            x_delta_l = []
            # 13.6. Influence:
            x_infl_l = []
            # 13.7. Atomic influence:
            x_atom_infl_l = []
            # 13.8. One order distance coefficient:
            x_pos_dis_coef_l = []
            # 13.9. Pair-mean one order distance coefficient:
            x_pair_mean_pos_dis_coef_l = []
            # 13.10. Negative one order distance coefficient:
            x_neg_dis_coef_l = []
            # 13.11. Pair-mean negative one order distance coefficient:
            x_pair_mean_neg_dis_coef_l = []
            # 13.12. Sum of one order gradient:
            x_sum_grad_l = []
            # 13.13. Pair-mean one order gradient:
            x_pair_mean_grad_l = []
            # 13.14. Max distance ratio of fragment pairs:
            x_dis_ratio_l = []
            # 13.15. Potential energy:
            # x_u_l = []
            # 13.16. Sum of two order gradient:
            x_sum_laplace_l = []
            # 13.17. Pair-mean two order gradient:
            x_pair_mean_laplace_l = []
            # Properties calculation:
            for r in ring_list:
                a_p_l = [atom_props_list[a] for a in r]
                x_count_l.append(sum(a_p_l))  # 1.
                x_atom_mean_l.append(sum(a_p_l) / len(r))  # 2.
                frag_x = []
                frag_atom_id = []
                for i in range(len(mff_title_list)):
                    patt = mff_title_list[i]
                    f = Chem.MolFromSmarts(patt)
                    atomids = mol.GetSubstructMatches(f)
                    if len(atomids) > 0:
                        for j in range(len(atomids)):
                            peoe_flag = True
                            for k in atomids[j]:
                                if k not in r:
                                    peoe_flag = False
                                    break
                            if peoe_flag:
                                frag_atom_id.append(atomids[j])
                                x_temp = 0
                                for k in atomids[j]:
                                    x_temp += atom_props_list[k]
                                frag_x.append(x_temp)
                for j in range(len(r)):
                    atom_id = r[j]
                    frag_x.append(atom_props_list[atom_id])
                    frag_atom_id.append([atom_id])
                x_max_l.append(max(frag_x))  # 3.
                x_min_l.append(min(frag_x))  # 4.
                x_delta_l.append(max(frag_x) - min(frag_x))  # 5.
                f_1 = [i for i in frag_atom_id[frag_x.index(min(frag_x))]]
                f_2 = [i for i in frag_atom_id[frag_x.index(max(frag_x))]]
                s = np.max(d_m[f_1, :][:, f_2]) / np.max(d_m[r, :][:, r])
                x_dis_ratio_l.append(s)  # 14.
                # Calculate the influence.
                temp_infl = 0
                for a in r:
                    temp_infl += atom_props_list[a] * atoms[a].GetDegree()
                x_infl_l.append(temp_infl)  # 6.
                x_atom_infl_l.append(temp_infl / len(r))  # 7.
                # Calculate the distance index and one or two order gradients.
                ttp = 0
                tti = 0
                grad_temp = 0
                laplace_temp = 0
                count = 0
                for i in range(len(r)):
                    for j in range(len(r) - i - 1):
                        a = r[i]
                        b = r[i + j + 1]
                        count += 1
                        a_e = atom_props_list[a]
                        b_e = atom_props_list[b]
                        ttp += a_e * b_e * d_m[a, b]
                        tti += a_e * b_e / d_m[a, b]
                        grad_temp += abs(a_e - b_e) / d_m[a, b]
                        laplace_temp += abs(a_e - b_e) / (d_m[a, b] ** 2)
                x_pos_dis_coef_l.append(ttp)  # 8.
                x_pair_mean_pos_dis_coef_l.append(ttp / count)  # 9.
                x_neg_dis_coef_l.append(tti)  # 10.
                x_pair_mean_neg_dis_coef_l.append(tti / count)  # 11.
                x_sum_grad_l.append(grad_temp)  # 12.
                x_pair_mean_grad_l.append(grad_temp / count)  # 13.
                x_sum_laplace_l.append(laplace_temp)  # 16.
                x_pair_mean_laplace_l.append(laplace_temp / count)  # 17.
            conju_props.append(x_count_l)
            conju_props.append(x_atom_mean_l)
            conju_props.append(x_max_l)
            conju_props.append(x_min_l)
            conju_props.append(x_delta_l)
            conju_props.append(x_infl_l)
            conju_props.append(x_atom_infl_l)
            conju_props.append(x_pos_dis_coef_l)
            conju_props.append(x_pair_mean_pos_dis_coef_l)
            conju_props.append(x_neg_dis_coef_l)
            conju_props.append(x_pair_mean_neg_dis_coef_l)
            conju_props.append(x_sum_grad_l)
            conju_props.append(x_pair_mean_grad_l)
            conju_props.append(x_dis_ratio_l)
            conju_props.append(x_sum_laplace_l)
            conju_props.append(x_pair_mean_laplace_l)
        for i in range(len(conju_props)):
            index = 5 + i
            if keep_type == 'max':
                data_conju[_, index] = conju_props[i][conju_size_list.index(max(conju_size_list))]
            elif keep_type == 'mean':
                data_conju[_, index] = np.mean(conju_props[i])
            elif keep_type == 'acc-mean':
                temp = 0
                for j in range(len(conju_size_list)):
                    temp += conju_size_list[j] * conju_props[i][j]
                data_conju[_, index] = temp / sum(conju_size_list)
    x = data_conju
    title = np.array(CONJU_TITLE).reshape(len(CONJU_TITLE), 1)
    return x, title


def NormMolFeat(smiles_rd, mff_title_list=None):
    """
    Generate 'Conjugation' descriptor matrix for the whole molecule, not only the conjugation structure.

    :param smiles_rd: List of SMILES string of molecules
    :param mff_title_list: List of MFF titles, needed for calculation, default as None

    :return: A tuple of (X, title)
             X: numpy array with shape of (len(smiles_rd), num_of_features)
             title: numpy array with shape of (num_of_features, 1)

    example:
    X_norm, title_norm = DChemPy.Featurization.NormMolFeat(smiles_list, mff_title_list=mff_title_list)
    """
    if type(smiles_rd) is np.ndarray:
        smiles_rd = list(smiles_rd.flatten())
    if type(mff_title_list) is np.ndarray:
        mff_title_list = list(mff_title_list.flatten())
    # For MOE-like VSA Descriptors:
    dij_m = np.zeros((54, 54))
    ri_m = np.zeros((54, 1))
    ri_m[6, 0] = 1.950  # C
    ri_m[7, 0] = 1.950  # N
    ri_m[8, 0] = 1.779  # O
    ri_m[9, 0] = 1.496  # F
    ri_m[15, 0] = 2.287  # P
    ri_m[16, 0] = 2.185  # S
    ri_m[17, 0] = 2.044  # Cl
    ri_m[35, 0] = 2.166  # Br
    ri_m[53, 0] = 2.358  # I
    dij_m[6, 35] = 1.970  # C-Br
    dij_m[35, 6] = 1.970
    dij_m[7, 35] = 1.840  # N-Br
    dij_m[35, 7] = 1.840
    dij_m[6, 6] = 1.540  # C-C
    dij_m[7, 7] = 1.450  # N-N
    dij_m[8, 8] = 1.470  # O-O
    dij_m[6, 17] = 1.800  # C-Cl
    dij_m[17, 6] = 1.800
    dij_m[6, 9] = 1.350  # C-F
    dij_m[9, 6] = 1.350
    dij_m[6, 53] = 2.120  # C-I
    dij_m[53, 6] = 2.120
    dij_m[6, 7] = 1.470  # C-N
    dij_m[7, 6] = 1.470
    dij_m[6, 8] = 1.430  # C-N
    dij_m[8, 6] = 1.430
    dij_m[6, 15] = 1.850  # C-P
    dij_m[15, 6] = 1.850
    dij_m[6, 16] = 1.810  # C-S
    dij_m[16, 6] = 1.810
    dij_m[7, 8] = 1.460  # N-O
    dij_m[8, 7] = 1.460
    dij_m[7, 15] = 1.600  # N-P
    dij_m[15, 7] = 1.600
    dij_m[7, 16] = 1.760  # N-S
    dij_m[16, 7] = 1.760
    dij_m[8, 15] = 1.570  # O-P
    dij_m[15, 8] = 1.570
    dij_m[8, 16] = 1.570  # O-S
    dij_m[16, 8] = 1.570

    def find_elec_num(kind, hyb_t):
        one_list = ['C']
        two_list = ['N', 'O', 'S', 'P', 'F', 'Cl', 'Br', 'I']
        if kind in one_list:
            return 1
        elif kind in two_list:
            if hyb_t == 'SP' and kind in ['N', 'P', 'O']:
                return 1
            elif hyb_t == 'SP2' and kind in ['N', 'O', 'S']:
                return 1
            else:
                return 2

    CONJU_TITLE = []
    CONJU_PRE = ['Apperant-Elec-Count', 'PEOE-Charge', 'EState-Indice', 'Atomic-LogP', 'Atomic-MR']
    CONJU_NUM = 1 + 5 + 16 * len(CONJU_PRE)
    data_conju = np.zeros((len(smiles_rd), CONJU_NUM))
    descList = []
    allowedDescriptors = ['MolWt']
    for descriptor, function in Descriptors.descList:
        if descriptor in allowedDescriptors:
            descList.append((descriptor, function))

    for _ in range(len(smiles_rd)):
        smi = smiles_rd[_]
        mol = Chem.MolFromSmiles(Chem.MolToSmiles(Chem.MolFromSmiles(smi)))
        atoms = mol.GetAtoms()
        a_m = Chem.rdmolops.GetAdjacencyMatrix(mol)
        d_m = Chem.rdmolops.GetDistanceMatrix(mol)
        ring_list = [[a.GetIdx() for a in atoms]]
        f_a = [a.GetIdx() for a in atoms]
        conju_size_list = [len(r) for r in ring_list]
        # Calculate apparent conjugation charges:
        app_elec = []
        for a in range(len(atoms)):
            if a in f_a:
                a_kind = atoms[a].GetSymbol()
                hyb = str(atoms[a].GetHybridization())
                app_elec.append(find_elec_num(a_kind, hyb))
            else:
                app_elec.append(0)
        # Calculate PEOE Charges:
        AllChem.ComputeGasteigerCharges(mol, nIter=25)
        peoe_charge = [mol.GetAtomWithIdx(i).GetDoubleProp('_GasteigerCharge') for i in range(mol.GetNumAtoms())]
        # Calculate EState Indices:
        estate_index = EStateIndices(mol)
        # Calculate atomic contribution of LogP and MR:
        contribs = rdMolDescriptors._CalcCrippenContribs(mol)
        logp = [contribs[i][0] for i in range(len(contribs))]
        mr = [contribs[i][1] for i in range(len(contribs))]

        atom_props = [app_elec, peoe_charge, estate_index, logp, mr]

        if _ == 0:
            CONJU_TITLE.append('Num of Conju-Stru (MFF-Conju)')  # 1.
            CONJU_TITLE.append('Num of Conju-All-Atoms (MFF-Conju)')  # 2.
            CONJU_TITLE.append('Atom Num Conju-All Ratio (MFF-Conju)')  # 3.
            CONJU_TITLE.append('AtomWt Conju-All Ratio (MFF-Conju)')  # 4.
            CONJU_TITLE.append('Full-Mol Wiener Index (MFF-Conju)')  # 5.
            CONJU_TITLE.append('Individual Conju-Atom Number (MFF-Conju)')  # 6.
            CONJU_TITLE.append('Conju-Part-Wt (MFF-Conju)')  # 7.
            CONJU_TITLE.append('Conju-AtomicWt (MFF-Conju)')  # 8.
            CONJU_TITLE.append('Max Conju-Distance (MFF-Conju)')  # 9.
            CONJU_TITLE.append('Conju-Branch Index (MFF-Conju)')  # 10.
            CONJU_TITLE.append('Conju-Stru Wiener Index (MFF-Conju)')  # 11.
            CONJU_TITLE.append('Conju-Stru-VSA (MFF-Conju)')  # 12.
        # 5. Wiener Index:
        if '.' in smi:
            mol22 = Chem.MolFromSmiles(smi.split('.')[0])
            dm22 = Chem.rdmolops.GetDistanceMatrix(mol22)
            data_conju[_, 0] = np.sum(dm22) / (2 * dm22.shape[0] * (dm22.shape[0] - 1))
        else:
            data_conju[_, 0] = np.sum(d_m) / (2 * d_m.shape[0] * (d_m.shape[0] - 1))

        # Indenpent features of conjugation structures:
        wt_list = []
        mwt_list = []
        for r in ring_list:
            tt = 0
            for a in r:
                tt += atoms[a].GetMass()
            wt_list.append(tt)
            mwt_list.append(tt / len(r))
        # 6. Atom numbers of individual conjugation structures:
        size_l = []
        for r in ring_list:
            size_l.append(len(r))
        data_conju[_, 1] = size_l[0]
        # 9. Size of individual conjugation structures:
        conju_max_dis = []
        for r in ring_list:
            conju_max_dis.append(np.max(d_m[r, :][:, r]))
        data_conju[_, 2] = conju_max_dis[0]

        # 10. Branching index of individual conjugation structures:
        branch_l = []
        for i in range(len(wt_list)):
            branch_l.append(np.sum(a_m[ring_list[i], :][:, ring_list[i]]) / (2 * size_l[i]))
        data_conju[_, 3] = branch_l[0]

        # 11. Weiner index of individual conjugation structures:
        wi_l = []
        for r in ring_list:
            d_m_temp = d_m[r, :][:, r]
            wi_l.append(np.sum(d_m_temp) / (2 * d_m_temp.shape[0] * (d_m_temp.shape[0] - 1)))
        data_conju[_, 4] = wi_l[0]

        # 12. VSA of individual conjugation structures:
        conju_vsa_l = []
        for r in ring_list:
            vsa_t = 0
            for i in range(len(r)):
                vsa_tt = 0
                atom = atoms[r[i]]
                n_l = atom.GetNeighbors()
                aid_1 = atom.GetAtomicNum()
                ar_1 = ri_m[aid_1, 0]
                for j in range(len(n_l)):
                    aid_2 = n_l[j].GetAtomicNum()
                    ar_2 = ri_m[aid_2, 0]
                    dij_i = dij_m[aid_1, aid_2]
                    dij = min(max(abs(ar_1 - ar_2), dij_i), ar_1 + ar_2)
                    vsa_tt += (ar_2 ** 2 - (ar_1 - dij) ** 2) / dij
                vsa_t += 4 * np.pi * ar_1 ** 2 - np.pi * ar_1 * vsa_tt
            conju_vsa_l.append(vsa_t)
        data_conju[_, 5] = conju_vsa_l[0]

        # Atomic Descriptors:
        for __ in range(len(atom_props)):
            PRE = 'Conju-' + CONJU_PRE[__] + '-'
            END_P = ' (MFF-Conju)'
            atom_props_list = atom_props[__]
            if _ == 0:
                CONJU_TITLE.append(PRE + 'Sum' + END_P)  # 13.1.
                CONJU_TITLE.append(PRE + 'AtomicMean' + END_P)  # 13.2.
                CONJU_TITLE.append(PRE + 'Maximum' + END_P)  # 13.3.
                CONJU_TITLE.append(PRE + 'Minimum' + END_P)  # 13.4.
                CONJU_TITLE.append(PRE + 'Delta' + END_P)  # 13.5.
                CONJU_TITLE.append(PRE + 'Influence' + END_P)  # 13.6.
                CONJU_TITLE.append(PRE + 'AtomicInfluence' + END_P)  # 13.7.
                CONJU_TITLE.append(PRE + 'PositiveDisCoef' + END_P)  # 13.8.
                CONJU_TITLE.append(PRE + 'PairMean-PositiveDisCoef' + END_P)  # 13.9.
                CONJU_TITLE.append(PRE + 'NegativeDisCoef' + END_P)  # 13.10.
                CONJU_TITLE.append(PRE + 'PairMean-NegativeDisCoef' + END_P)  # 13.11.
                CONJU_TITLE.append(PRE + 'GradSum' + END_P)  # 13.12.
                CONJU_TITLE.append(PRE + 'PairMean-Grad' + END_P)  # 13.13.
                CONJU_TITLE.append(PRE + 'MaxMinDisRatio' + END_P)  # 13.14.
                # CONJU_TITLE.append(PRE+'AppearantU'+END_P)  # 13.15.
                CONJU_TITLE.append(PRE + 'LaplaceSum' + END_P)  # 13.16.
                CONJU_TITLE.append(PRE + 'PairMean-Laplace' + END_P)  # 13.17.
            # 13.1. Sum without fragment:
            x_count_l = []
            # 13.2. Atomic mean without fragments:
            x_atom_mean_l = []
            # 13.3. Maximum with fragments:
            x_max_l = []
            # 13.4. Minimum with fragments:
            x_min_l = []
            # 13.5. Max-Min with fragments:
            x_delta_l = []
            # 13.6. Influence:
            x_infl_l = []
            # 13.7. Atomic influence:
            x_atom_infl_l = []
            # 13.8. One order distance coefficient:
            x_pos_dis_coef_l = []
            # 13.9. Pair-mean one order distance coefficient:
            x_pair_mean_pos_dis_coef_l = []
            # 13.10. Negative one order distance coefficient:
            x_neg_dis_coef_l = []
            # 13.11. Pair-mean negative one order distance coefficient:
            x_pair_mean_neg_dis_coef_l = []
            # 13.12. Sum of one order gradient:
            x_sum_grad_l = []
            # 13.13. Pair-mean one order gradient:
            x_pair_mean_grad_l = []
            # 13.14. Max distance ratio of fragment pairs:
            x_dis_ratio_l = []
            # 13.15. Potential energy:
            # x_u_l = []
            # 13.16. Sum of two order gradient:
            x_sum_laplace_l = []
            # 13.17. Pair-mean two order gradient:
            x_pair_mean_laplace_l = []
            # Properties calculation:
            for r in ring_list:
                a_p_l = [atom_props_list[a] for a in r]
                x_count_l.append(sum(a_p_l))  # 1.
                x_atom_mean_l.append(sum(a_p_l) / len(r))  # 2.
                frag_x = []
                frag_atom_id = []
                for i in range(len(mff_title_list)):
                    patt = mff_title_list[i]
                    f = Chem.MolFromSmarts(patt)
                    atomids = mol.GetSubstructMatches(f)
                    if len(atomids) > 0:
                        for j in range(len(atomids)):
                            peoe_flag = True
                            for k in atomids[j]:
                                if k not in r:
                                    peoe_flag = False
                                    break
                            if peoe_flag:
                                frag_atom_id.append(atomids[j])
                                x_temp = 0
                                for k in atomids[j]:
                                    x_temp += atom_props_list[k]
                                frag_x.append(x_temp)
                for j in range(len(r)):
                    atom_id = r[j]
                    frag_x.append(atom_props_list[atom_id])
                    frag_atom_id.append([atom_id])
                x_max_l.append(max(frag_x))  # 3.
                x_min_l.append(min(frag_x))  # 4.
                x_delta_l.append(max(frag_x) - min(frag_x))  # 5.
                f_1 = [i for i in frag_atom_id[frag_x.index(min(frag_x))]]
                f_2 = [i for i in frag_atom_id[frag_x.index(max(frag_x))]]
                s = np.max(d_m[f_1, :][:, f_2]) / np.max(d_m[r, :][:, r])
                x_dis_ratio_l.append(s)  # 14.
                # Calculate the influence.
                temp_infl = 0
                for a in r:
                    temp_infl += atom_props_list[a] * atoms[a].GetDegree()
                x_infl_l.append(temp_infl)  # 6.
                x_atom_infl_l.append(temp_infl / len(r))  # 7.
                # Calculate the distance index and one or two order gradients.
                ttp = 0
                tti = 0
                grad_temp = 0
                laplace_temp = 0
                count = 0
                for i in range(len(r)):
                    for j in range(len(r) - i - 1):
                        a = r[i]
                        b = r[i + j + 1]
                        count += 1
                        a_e = atom_props_list[a]
                        b_e = atom_props_list[b]
                        ttp += a_e * b_e * d_m[a, b]
                        tti += a_e * b_e / d_m[a, b]
                        grad_temp += abs(a_e - b_e) / d_m[a, b]
                        laplace_temp += abs(a_e - b_e) / (d_m[a, b] ** 2)
                x_pos_dis_coef_l.append(ttp)  # 8.
                x_pair_mean_pos_dis_coef_l.append(ttp / count)  # 9.
                x_neg_dis_coef_l.append(tti)  # 10.
                x_pair_mean_neg_dis_coef_l.append(tti / count)  # 11.
                x_sum_grad_l.append(grad_temp)  # 12.
                x_pair_mean_grad_l.append(grad_temp / count)  # 13.
                x_sum_laplace_l.append(laplace_temp)  # 16.
                x_pair_mean_laplace_l.append(laplace_temp / count)  # 17.
            data_conju[_, 6+16*__] = x_count_l[0]
            data_conju[_, 7+16*__] = x_atom_mean_l[0]
            data_conju[_, 8+16*__] = x_max_l[0]
            data_conju[_, 9+16*__] = x_min_l[0]
            data_conju[_, 10+16*__] = x_delta_l[0]
            data_conju[_, 11+16*__] = x_infl_l[0]
            data_conju[_, 12+16*__] = x_atom_infl_l[0]
            data_conju[_, 13+16*__] = x_pos_dis_coef_l[0]
            data_conju[_, 14+16*__] = x_pair_mean_pos_dis_coef_l[0]
            data_conju[_, 15+16*__] = x_neg_dis_coef_l[0]
            data_conju[_, 16+16*__] = x_pair_mean_neg_dis_coef_l[0]
            data_conju[_, 17+16*__] = x_sum_grad_l[0]
            data_conju[_, 18+16*__] = x_pair_mean_grad_l[0]
            data_conju[_, 19+16*__] = x_dis_ratio_l[0]
            data_conju[_, 20+16*__] = x_sum_laplace_l[0]
            data_conju[_, 21+16*__] = x_pair_mean_laplace_l[0]
    x = data_conju
    title = np.array(CONJU_TITLE).reshape(len(CONJU_TITLE), 1)
    return x, title


def PeptideFeat(pep_list):
    """
    Generate simple amino acid index for peptides
    All amino piece should be represented as numbers as below:
    ref = {'O': 0, 'G': 1, 'A': 2, 'V': 3, 'L': 4, 'I': 5, 'M': 6, 'C': 7, 'T': 8, 'S': 9,
           'N': 10, 'Q': 11, 'D': 12, 'E': 13, 'F': 14, 'Y': 15, 'W': 16, 'H': 17, 'P': 18, 'K': 19, 'R': 20}

    :param pep_list: List of peptide sequence, for example ['A.G.H.C.T', 'V.M.A.Q']

    :return: A tuple of (X, title)
             X: numpy array with shape of (len(pep_list), max_num_of_amino_pieces)
             title: numpy array with shape of (max_num_of_amino_pieces, 1)

    example:
    X_pep, title_pep = DChemPy.Featurization.PeptideFeat(pep_list)
    """
    if type(pep_list) is np.ndarray:
        pep_list = list(pep_list.flatten())
    ref = {'O': 0, 'G': 1, 'A': 2, 'V': 3, 'L': 4, 'I': 5, 'M': 6, 'C': 7, 'T': 8, 'S': 9,
           'N': 10, 'Q': 11, 'D': 12, 'E': 13, 'F': 14, 'Y': 15, 'W': 16, 'H': 17, 'P': 18, 'K': 19, 'R': 20}
    max_length = max([len(p) for p in pep_list])
    data = np.zeros((len(pep_list), max_length))
    for i in range(len(pep_list)):
        pep = pep_list[i]
        amino = pep.split('.')
        for j in range(len(amino)):
            data[i, j] = ref[amino[j]]
    x = data
    title = np.array(['A'+str(i+1) for i in range(max_length)]).reshape(max_length, 1)
    return x, title


def PeptideToSmi(pep_list):
    """
    Turn a list of peptide into a list of SMILES

    :param pep_list: List of peptide sequence, for example ['A.G.H.C.T', 'V.M.A.Q']

    :return: smiles_list

    example:
    smi_list = DChemPy.Featurization.PeptideToSmi(pep_list)
    """
    smi_list = []
    for pep in pep_list:
        s = 'PEPTIDE1{' + pep + '}$$$$'
        mol = Chem.MolFromHELM(s)
        smi = Chem.MolToSmiles(mol)
        smi_list.append(smi)
    smi_list = np.array(smi_list).reshape(len(smi_list), 1)
    return smi_list


def CombineX(X_list):
    """
    Connect a series of X in X_list

    :param X_list: list of X matrix, for example [X_mff, X_rdkit, X_conju]

    :return: X

    example:
    X_out =  DChemPy.Featurization.CombineX([X_mff, X_rdkit, X_conju])
    """
    X = X_list[0]
    if len(X_list) >= 2:
        for i in range(len(X_list) - 1):
            X = np.hstack((X, X_list[i + 1]))
    return X


def CombineTitle(title_list):
    """
    Connect a series of title in title_list

    :param title_list: list of title, for example [title_mff, title_rdkit, title_conju]

    :return: title
    note: output title matrix with shape of (total_num_features, 1)

    example:
    title_out =  DChemPy.Featurization.CombineTitle([title_mff, title_rdkit, title_conju])
    """
    for i in range(len(title_list)):
        if type(title_list[i]) is np.ndarray:
            title_list[i] = title_list[i].reshape(title_list[i].shape[0], 1)
        elif type(title_list[i]) is list:
            title_list[i] = np.array(title_list[i]).reshape(len(title_list[i]), 1)
    title_init = title_list[0]
    if len(title_list) >= 2:
        for i in range(len(title_list) - 1):
            title_init = np.vstack((title_init, title_list[i + 1]))
    return title_init


def CheckDataset(x, y, title, smiles=None):
    """
    Check the dataset: delete rows with nan & inf, delete columns with maximum==minimum

    :param x: Feature Matrix
    :param y: Label Values with type of numpy.array and shape of (num_samples, 1)
    :param title: Title with type of numpy.array and shape of (num_features, 1)
    :param smiles: SMILES array with type of numpy.array and shape of (num_samples, 1), optional, default as None

    :return: Tuple of (x, y, title) or (x, y, title, smiles)

    example:
    X_out, y_out, title_out = DChemPy.Featurization.CheckDataset(X, y, title)
    X_out, y_out, title_out, smiles_out = DChemPy.Featurization.CheckDataset(X, y, title, smiles)
    """
    if type(y) is np.ndarray:
        y = y.reshape(y.shape[0], 1)
    elif type(y) is list:
        y = np.array(y).reshape(len(y), 1)
    if type(title) is np.ndarray:
        title = title.reshape(title.shape[0], 1)
    elif type(y) is list:
        y = np.array(y).reshape(len(y), 1)
    if smiles is not None:
        if type(smiles) is np.ndarray:
            smiles = smiles.reshape(smiles.shape[0], 1)
        elif type(smiles) is list:
            smiles = np.array(smiles).reshape(len(smiles), 1)
    del_list_row = []
    for i in range(x.shape[0]):
        if (np.isnan(x[i, :].astype(float)).sum() > 0) or (np.inf in x[i, :].astype(float)):
            del_list_row.append(i)
            continue
    del_list_col = []
    for i in range(x.shape[1]):
        if max(x[:, i].astype(float)) == min(x[:, i].astype(float)):
            del_list_col.append(i)
            continue
    x = np.delete(x, del_list_row, axis=0)
    x = np.delete(x, del_list_col, axis=1)
    y = np.delete(y, del_list_row, axis=0)
    title = np.delete(title, del_list_col, axis=0)
    if smiles is None:
        return x, y, title
    else:
        smiles = np.delete(smiles, del_list_row, axis=0)
        return x, y, title, smiles


def MakeSaveY(y, value_ln=False, value_div_weight=False, smiles=None, directory=None, notes=''):
    """
    Turn Y into ln(y), y/MolWt, ln(y/MolWt)

    :param y: Label Values with type of numpy.array and shape of (num_samples, 1)
    :param value_ln: Whether to calculate ln(y), default as 'False'
    :param value_div_weight: Whether to calculate y/MolWt, default as 'False'.
                             If set to 'True', smiles should be input.
    :param smiles: List of SMILES, default as 'None'
    :param directory: Directory to save outputs, default as 'None', for example 'data_out'
    :param notes: Notes in file name, default as '', for example '_True'

    :return: None

    example:
    DChemPy.Featurization.MakeSaveY(y, value_ln=True, note='_True')
    DChemPy.Featurization.MakeSaveY(y, value_ln=True, directory='data_out', note='_True')
    DChemPy.Featurization.MakeSaveY(y, value_ln=True, value_div_weight=True, smiles=smiles_list,
                                    directory='data_out', note='_True')
    """
    if type(y) is np.ndarray:
        y = y.reshape(y.shape[0], 1)
    elif type(y) is list:
        y = np.array(y).reshape(len(y), 1)
    if type(smiles) is np.ndarray:
        smiles = list(smiles.flatten())
    if value_div_weight:
        values_rd_dwt = []
        for descriptor, function in Descriptors.descList:
            if descriptor == 'MolWt':
                for i in range(len(smiles)):
                    smile = smiles[i]
                    mol = Chem.MolFromSmiles(str(smile))
                    v = y[i, 0] / function(mol)
                    values_rd_dwt.append(v)
        values_dwt_out = np.array(values_rd_dwt).reshape(len(values_rd_dwt), 1)
    if directory is None:
        np.savetxt('Values'+notes+'_'+str(y.shape[0])+'.csv', y, fmt='%s', delimiter=',')
        if value_ln:
            np.savetxt('Values' + notes + '_ln_' + str(y.shape[0]) + '.csv', np.log(y), fmt='%s', delimiter=',')
        if value_div_weight:
            np.savetxt('Values' + notes + '_wt_' + str(y.shape[0]) + '.csv', values_dwt_out,
                       fmt='%s', delimiter=',')
    else:
        if not os.path.exists(directory):
            os.mkdir(directory)
        save_name = Path('', directory, 'Values' + notes + '_' + str(y.shape[0]) + '.csv')
        np.savetxt(save_name, y, fmt='%s', delimiter=',')
        if value_ln:
            save_name = Path('', directory, 'Values' + notes + '_ln_' + str(y.shape[0]) + '.csv')
            np.savetxt(save_name, np.log(y), fmt='%s', delimiter=',')
        if value_div_weight:
            save_name = Path('', directory, 'Values' + notes + '_w_' + str(y.shape[0]) + '.csv')
            np.savetxt(save_name, values_dwt_out, fmt='%s', delimiter=',')


def SaveXSmiTitle(x, smiles, title, directory=None, notes=''):
    """
    Save X, Smiles and Title

    :param x: Feature Matrix
    :param smiles: SMILES with type of numpy.array and shape of (num_samples, 1)
    :param title: Title with type of numpy.array and shape of (num_featrues, 1)
    :param directory: Directory to save outputs, default as 'None', for example 'data_out'
    :param notes: Notes in file name, default as ''

    :return: None

    example:
    DChemPy.Featurization.SaveXSmiTitle(X_out, smiles_out, title_out)
    DChemPy.Featurization.SaveXSmiTitle(X_out, smiles_out, title_out, directory='data_out')
    """
    if type(smiles) is np.ndarray:
        smiles = smiles.reshape(smiles.shape[0], 1)
    elif type(smiles) is list:
        smiles = np.array(smiles).reshape(len(smiles), 1)
    if type(title) is np.ndarray:
        title = title.reshape(title.shape[0], 1)
    elif type(title) is list:
        title = np.array(title).reshape(len(title), 1)
    if directory is None:
        np.savetxt('Features'+notes+'_'+str(x.shape[0])+'_'+str(x.shape[1])+'.csv', x, fmt='%s', delimiter=',')
        np.savetxt('Smiles'+notes+'_'+str(smiles.shape[0])+'.csv', smiles, fmt='%s', delimiter=',')
        np.savetxt('Titles'+notes+'_'+str(title.shape[0])+'.csv', x, fmt='%s', delimiter=',')
    else:
        if not os.path.exists(directory):
            os.mkdir(directory)
        save_name = Path('', directory, 'Features' + notes + '_' + str(x.shape[0]) + '_' + str(x.shape[1]) + '.csv')
        np.savetxt(save_name, x, fmt='%s', delimiter=',')
        save_name = Path('', directory, 'Smiles' + notes + '_' + str(smiles.shape[0]) + '.csv')
        np.savetxt(save_name, smiles, fmt='%s', delimiter=',')
        save_name = Path('', directory, 'Titles' + notes + '_' + str(title.shape[0]) + '.csv')
        np.savetxt(save_name, title, fmt='%s', delimiter=',')
