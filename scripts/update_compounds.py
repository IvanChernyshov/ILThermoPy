'''This script contains functionality to update structural information (SMILES)
of ILThermo compounds after database is updated.

Structural information of ILThermo compounds is stored in a table format
in the _compounds.csv_ file. It contains:
    
    * compound id (internal ILThermo parameter);
    
    * compound name (internal ILThermo parameter);
    
    * manually checked SMILES string of the compound.

Please note that ILThermo updates change compound ids,
thus they can not be used to link old and new versions of compound lists.

This script works in the following way:
    
    1. Loads the old version of compound list from the latest version of the _ilthermopy_ package;
    
    2. Loads the new version of compound list from the ILThermo database;
    
    3. Compares datasets by compound name and extracts missing compounds (with no SMILES);
    
    4. Uses OPSIN and PubChem to convert chemical names to SMILES;
    
    5. Creates CSV and PNG files for quick verification of automatically retrieved and manually provided SMILES strings;
    
    6. Prepares the final version of _compounds.csv_ to use in the new _ilthermopy_ version.

'''

#%% Imports

import os, sys, warnings
from PIL import Image, ImageDraw, ImageFont

from tqdm import tqdm

import pandas as pd

from py2opsin import py2opsin
import pubchempy as pcp

from rdkit import Chem
from rdkit.Chem.Draw import MolToImage

import ilthermopy as ilt
from ilthermopy.requests import GetCompoundImage


#%% Functions

def get_current_compounds():
    '''Returns info on current compounds'''
    # retrieve data
    data = ilt.GetAllEntries()
    # extract compounds
    dfs = []
    for i in range(1, 4):
        df = data[[f'cmp{i}_id', f'cmp{i}', f'cmp{i}_smiles']]
        df.columns = ['id', 'name', 'smiles']
        df = df.loc[~df['id'].isna()]
        df = df.drop_duplicates(ignore_index = True)
        dfs.append(df)
    # combine compounds #1-#3
    df = pd.concat(dfs, ignore_index = True).drop_duplicates(ignore_index = True)
    
    return df


def get_smiles_opsin(names):
    '''Uses OPSIN to get SMILES for the given chemical names'''
    warnings.filterwarnings('ignore')
    smis = py2opsin(chemical_name = names, output_format = 'SMILES',
                    allow_acid = True, allow_radicals = False)
    warnings.filterwarnings('default')
    
    return smis


def get_smiles_pubchem(names):
    '''Uses PubChem to get SMILES for the given chemical names'''
    smis = []
    for name in tqdm(names):
        # skip if no name
        if not name:
            smis.append('')
            continue
        # retrieve compounds
        cmps = pcp.get_compounds(name, 'name')
        if not cmps:
            smis.append('')
            continue
        # get smiles
        smis.append( cmps[0].canonical_smiles )
    
    return smis


def name2smiles(names):
    '''Uses PubChem and OPSIN to get SMILES for the give chemical names'''
    smis_opsin = get_smiles_opsin(miss.name)
    smis_pubchem = get_smiles_pubchem(miss.name)
    smis = []
    for smi_ops, smi_pub in zip(smis_opsin, smis_pubchem):
        if not smi_ops and not smi_pub:
            smi = ''
        elif not smi_ops and smi_pub:
            smi = smi_pub
        elif smi_ops and not smi_pub:
            smi = smi_ops
        else:
            smi = smi_pub
        smis.append(smi)
    
    return smis


def save_compounds_images(cids, path_dir):
    '''Saves compound image to the file'''
    for i, cid in tqdm(enumerate(cids), total = len(cids)):
        path = os.path.join(path_dir, f'{i:04d}_{cid}.png')
        image_data = GetCompoundImage(cid)
        with open(path, 'wb') as outf:
            outf.write(image_data)
    
    return


def get_total_charge(mol):
    '''Returns total formal charge of the given molecule'''
    
    return sum([a.GetFormalCharge() for a in mol.GetAtoms()])


def check_reviewed_structures(df):
    '''Basic chemoinformatical checks of provided SMILES'''
    # get mols
    mols = {}
    for i, (cid, smiles) in enumerate(zip(df['id'], df['smiles'])):
        mol = Chem.MolFromSmiles(smiles)
        mols[(i, cid)] = mol
    # check empty mols
    bad_mols = []
    for (i, cid), mol in mols.items():
        if not mol:
            bad_mols.append( (i, cid) )
    if not bad_mols:
        print('All SMILES are readable')
    else:
        print('Several unreadable smiles were detected:')
        for i, cid in bad_mols:
            print(i, cid)
        print()
    # check total charge
    bad_charge = []
    for (i, cid), mol in mols.items():
        q = get_total_charge(mol)
        if q:
            bad_charge.append( (i, cid) )
    if not bad_charge:
        print('All molecules are neutral')
    else:
        print('Several charged molecules were detected:')
        for i, cid in bad_charge:
            print(i, cid)
        print()
    
    return


def get_compound_images_paths(dir_img):
    '''Returns cid => path dictionary'''
    outp = {}
    for f in os.listdir(dir_img):
        cid = f.replace('.png', '').split('_')[1]
        outp[cid] = os.path.join(dir_img, f)
    
    return outp


def make_check_image(name, smiles, path_png):
    '''Combines DB and RDKit images'''
    # prepare mol-from-smiles image
    if not smiles:
        my_img = Image.new('RGBA', (500, 500), (255, 255, 255, 255))
    else:
        mol = Chem.MolFromSmiles(smiles)
        if not mol:
            my_img = Image.new('RGBA', (500, 500), (255, 255, 255, 255))
        else:
            my_img = MolToImage(mol, size = (500, 500))
    # prepare internal image
    db_img = Image.open(path_png)
    w, h = [int(500*x/max(db_img.size)) for x in db_img.size]
    if w >= h:
        db_x = 500
        db_y = 50 + int((500-h)/2)
    else:
        db_x = 500 + int((500-w)/2)
        db_y = 50
    db_img = db_img.resize((w, h), Image.LANCZOS)
    # make combined image
    img = Image.new('RGBA', (1000, 550), (255, 255, 255, 255))
    img.paste(my_img, (0, 50))
    try:
        img.paste(db_img, (db_x, db_y), mask = db_img.split()[-1])
    except ValueError:
        img.paste(db_img, (db_x, db_y))
    # add text
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default(size = 25)
    draw.text(xy = (10, 10), text = name, fill = (0, 0, 0), font = font)
    
    return img


#%% Main

if __name__ == '__main__':
    
    # paths
    path_data = 'data'
    path_old = 'data/old.csv'
    path_miss = 'data/missing.csv'
    path_man = 'data/missing_manual.csv'
    path_fin = 'data/final.csv'
    path_img = 'data/compound_images'
    path_check = 'data/check_images'
    
    # if there's no file for manual check
    if not os.path.exists(path_man):
        
        # get data
        print('\nLoading data ...')
        df = get_current_compounds()
        cmps = ilt.GetCompounds().data
        
        # get missing data
        print('\nPreparing missing compounds ...')
        miss = df.loc[~df.name.isin(cmps.name)].reset_index(drop = True)
        miss.loc[miss.name.isna(), 'name'] = ''
        if not os.path.exists(path_data):
            os.mkdir(path_data)
        
        # save untouched data
        print('Saving unchanged data ...')
        old = df.loc[df.name.isin(cmps.name)].reset_index(drop = True)
        old.to_csv(path_old, index = None)
        
        # retrieve SMILES for manual check
        print('\nRetrieving SMILES ...')
        smis = name2smiles(miss.name)
        miss['smiles'] = smis
        miss.to_csv(path_miss, index = None)
    
        # download images of missing compounds
        print('\n\nLoading compounds\' images ...')
        if not os.path.exists(path_img):
            os.mkdir(path_img)
        for f in os.listdir(path_img):
            os.remove(os.path.join(path_img, f))
        save_compounds_images(miss['id'], path_img)
        
        # stop script for manual review
        print('\n\nNow please provide smiles for the missing compounds\n')
        sys.exit(0)
    
    # loading data
    print('\nLoading data ...')
    old = pd.read_csv(path_old)
    add = pd.read_csv(path_man)
    add.loc[add.smiles.isna(), 'smiles'] = ''
    
    # generate images for manual revision
    print('\nGenerating images for manual review ...')
    cmp_images = get_compound_images_paths(path_img)
    if not os.path.exists(path_check):
        os.mkdir(path_check)
    else:
        for f in os.listdir(path_check):
            os.remove(os.path.join(path_check, f))
    for i, (cid, name, smiles) in tqdm(enumerate(zip(add['id'], add['name'], \
                                         add['smiles'])), total = len(add)):
        path_png = cmp_images[cid]
        path_out = os.path.join(path_check, f'{i:04d}_{cid}.png')
        img = make_check_image(name, smiles, path_png)
        img.save(path_out)
    
    # check SMILES quality
    print('\n\nChecking SMILES quality ...')
    check_reviewed_structures(add)
    
    # prepare new dataset
    print('\nGenerating final dataset ...')
    data = pd.concat([old, add])
    data = data.sort_values('id').reset_index(drop = True)
    data.to_csv(path_fin, index = None)
    
    # finita la comedia
    print('\nDone.\n')


