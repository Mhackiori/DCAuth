import os
import pandas as pd
import sys
import tsfresh

from utils.const import *
from utils.helperFunctions import *

import warnings
warnings.filterwarnings("ignore")

if not sys.warnoptions:
    warnings.simplefilter("ignore")
    os.environ["PYTHONWARNINGS"] = "ignore"  # Also affect subprocesses



# For every dataset in the processed folder
for dataset in DATASETS:
    print(f'[📚 DATASET] {dataset}')
    datasetDir = os.path.join(PROCESSED, dataset)

    # Checking if already processed
    chargeSave = os.path.join(datasetDir, 'charge.parquet')
    dischargeSave = os.path.join(datasetDir, 'discharge.parquet')

    if os.path.exists(chargeSave) and os.path.exists(dischargeSave):
        print(f'\t[✅ ALREADY PROCESSED]\n')
        continue

    feat_dfs_c = []
    feat_dfs_d = []
    for cycle in sorted(os.listdir(datasetDir)):
        # Skipping phase if partially processed
        if cycle == 'Charge' and os.path.exists(chargeSave):
            print(f'\t[✅ CHARGE ALREADY PROCESSED]')
            continue
        elif cycle == 'Disharge' and os.path.exists(dischargeSave):
            print(f'\t[✅ DISCHARGE ALREADY PROCESSED]\n')
            continue

        if cycle.split('.')[-1] != 'parquet':
            cycleDir = os.path.join(datasetDir, cycle)
            # Saving csv files as DataFrames
            for i, file in enumerate(os.listdir(cycleDir)):
                if cycle == 'Charge':
                    print(f'\t[🔋 PROCESSING] {i+1}/{len(os.listdir(cycleDir))}', end='\r')
                else:
                    print(f'\t[🪫 PROCESSING] {i+1}/{len(os.listdir(cycleDir))}', end='\r')
                filePath = os.path.join(cycleDir, file)
                df = pd.read_csv(filePath)
                df = df.drop('Unnamed: 0', axis=1)

                # Removing ID cols, but saving them for later
                id2 = df['id2']
                id3 = df['id3']
                df = df.drop(['id2', 'id3'], axis=1)
                # Extracting features
                features = tsfresh.extract_features(df, column_id="id1", column_sort="Voltage(V)", disable_progressbar=True)
                # Saving IDs
                features['id1'] = df['id1'][0] * len(features)
                features['id2'] = id2[0] * len(features)
                features['id3'] = id3[0] * len(features)

                if cycle == 'Charge':
                    feat_dfs_c.append(features)
                else:
                    feat_dfs_d.append(features)
                    
        if cycle == 'Charge':
            if not os.path.exists(chargeSave):
                df_c = pd.concat(feat_dfs_c)
                df_c.to_parquet(chargeSave)
        elif cycle == 'Disharge':
            if not os.path.exists(dischargeSave):
                df_d = pd.concat(feat_dfs_d)
                df_d.to_parquet(dischargeSave)

        print()
    
    if not os.path.exists(chargeSave):
        df_c = pd.concat(feat_dfs_c)
        df_c.to_parquet(chargeSave)

    if not os.path.exists(dischargeSave):
        df_d = pd.concat(feat_dfs_d)
        df_d.to_parquet(dischargeSave)

    print()
    print(f'\t[✅ SAVED]\n')