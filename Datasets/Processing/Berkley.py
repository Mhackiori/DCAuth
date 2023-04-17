# ID1: architecture (LCO = 2)
# ID2: model (Sanyo 18650 = 10)
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

    filePath = os.path.join(datasetDir, file)

    if file.split('.')[1] == 'csv'  and not processed:
        df = pd.read_csv(filePath)
        df['Charge_Capacity (Ah)'] = df['Charge Capacity (mAh)']/1000
        df['Discharge_Capacity (Ah)'] = df['Discharge Capacity (mAh)']/1000

        last_step = df['Step'][0]
        n_cycles = 0
        start_index = [0]
        end_index = []
        for i, step in enumerate(df['Step']):
            if step != last_step:
                n_cycles += 1
                last_step = step
                end_index.append(i-1)
                start_index.append(i)

        start_index = start_index[:-1]

        for cycle in range(len(start_index)):

            print(f'[🔢 {count}/{numFiles}] {cycle}/{len(start_index)}', end='\r')
            saveName = file.split('.')[0] + '_' + str(cycle) + '.csv'

            df_cycle = df.iloc[start_index[cycle]:end_index[cycle]]

            df_charge, df_discharge = dqdv(df_cycle, equip='Arbin_BA')

            voltage = 'Voltage (V)'
            # Ordering dQdV with respect to voltage
            dQdV_c = [x for _, x in sorted(
                zip(list(df_charge[voltage]), list(df_charge['dQ/dV'])))]

            dQdV_d = [x for _, x in sorted(
                zip(list(df_discharge[voltage]), list(df_discharge['dQ/dV'])))]

            # Constructing the DataFrame
            dfc = pd.DataFrame({
                'Voltage(V)': df_charge[voltage],
                'dQ/dV': dQdV_c
                })
            dfd = pd.DataFrame({
                'Voltage(V)': df_discharge[voltage],
                'dQ/dV':  dQdV_d
                })

            # Saving IDs
            dfc['id1'] = [2] * len(dQdV_c)
            dfd['id1'] = [2] * len(dQdV_d)

            dfc['id2'] = [10] * len(dQdV_c)
            dfd['id2'] = [10] * len(dQdV_d)

            dfc['id3'] = [df['Cell ID'][0]] * len(dQdV_c)
            dfd['id3'] = [df['Cell ID'][0]] * len(dQdV_d)

            # Saving processed data
            if len(dfc) > MIN_LENGTH:
                dfc.to_csv(os.path.join(chargeFolder, saveName))
            if len(dfd) > MIN_LENGTH:
                dfd.to_csv(os.path.join(dischargeFolder, saveName))

    count += 1

print()