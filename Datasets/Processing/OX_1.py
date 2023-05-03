# ID1: architecture (LCO = 2)
# ID2: model (PSLPB533459H4 = 7)
# ID3: cell sample

import os
import pandas as pd
import warnings

import sys
sys.path.insert(0, os.getcwd())

from utils.helperFunctions import *
from utils.const import *

warnings.filterwarnings("ignore")

if not sys.warnoptions:
    warnings.simplefilter("ignore")
    os.environ["PYTHONWARNINGS"] = "ignore"


datasetName = __file__.split('/')[-1].split('.')[0]
datasetDir = os.path.join(RAW, datasetName)

numFiles = sum(len(files) for _, _, files in os.walk(datasetDir))
files = sorted(os.listdir(datasetDir))

processedFolder = os.path.join(
    './Datasets/Processed/', datasetName)
chargeFolder = os.path.join(processedFolder, 'Charge')
dischargeFolder = os.path.join(
    processedFolder, 'Discharge')

if not os.path.exists(processedFolder):
    os.makedirs(processedFolder)
    os.makedirs(chargeFolder)
    os.makedirs(dischargeFolder)

count = 1

for file in files:
    processed = False
    for cf in os.listdir(chargeFolder):
        cf = cf.split('.')[0]
        if file.split('.')[0] in cf:
            processed = True
    for df in os.listdir(dischargeFolder):
        df = df.split('.')[0]
        if file.split('.')[0] in df:
            processed = True

    print(f'[🔢 {count}/{numFiles}] {file}', end='\r')
    filePath = os.path.join(datasetDir, file)

    if file.split('.')[1] == 'csv'  and not processed:
        df = pd.read_csv(filePath)

        # Putting dummy values for current to perform same processing
        if '_charge' in file.lower():
            df['Current(A)'] = [1] * len(df)
            df['Discharge_Capacity(Ah)'] = [0] * len(df)
        else:
            df['Current(A)'] = [-1] * len(df)
            df['Charge_Capacity(Ah)'] = [0] * len(df)

        # Extracting cycles
        n_cycles = df['Cycle_Index'].max()

        for cycle in range(n_cycles):
            saveName = file.split('.')[0] + '_' + str(cycle) + '.csv'
            df_cycle = df.loc[df['Cycle_Index'] == cycle+1]

            if '_charge' in file.lower():
                df_charge, _ = dqdv(df_cycle)

                # Ordering dQdV with respect to voltage
                dQdV_c = [x for _, x in sorted(
                    zip(list(df_charge['Voltage(V)']), list(df_charge['dQ/dV'])))]

                # Constructing the DataFrame
                dfc = pd.DataFrame({
                    'Voltage(V)': df_charge['Voltage(V)'],
                    'dQ/dV': dQdV_c
                })

                # Saving IDs
                dfc['id1'] = [2] * len(dQdV_c)
                dfc['id2'] = [7] * len(dQdV_c)
                dfc['id3'] = [int(file.split('_')[1][-1])] * len(dQdV_c)

                # Saving processed data
                if len(dfc) > MIN_LENGTH:
                    dfc.to_csv(os.path.join(chargeFolder, saveName))
            else:
                _, df_discharge = dqdv(df_cycle)

                # Ordering dQdV with respect to voltage
                dQdV_d = [x for _, x in sorted(
                    zip(list(df_discharge['Voltage(V)']), list(df_discharge['dQ/dV'])))]

                # Constructing the DataFrame
                dfd = pd.DataFrame({
                    'Voltage(V)': df_discharge['Voltage(V)'],
                    'dQ/dV': dQdV_d
                })

                # Saving IDs
                dfd['id1'] = [2] * len(dQdV_d)
                dfd['id2'] = [7] * len(dQdV_d)
                dfd['id3'] = [int(file.split('_')[1][-1])] * len(dQdV_d)

                # Saving processed data
                if len(dfd) > MIN_LENGTH:
                    dfd.to_csv(os.path.join(dischargeFolder, saveName))

    count += 1

print()