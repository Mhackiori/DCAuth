# ID1: architecture (LFP = 1)
# ID2: model (APR18650M1A = 5)
# ID3: batch(?)
import json
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

    if file.split('.')[1] == 'json' and not processed:
        # Loading file
        with open(filePath, "rb") as input_file:
            data = json.load(input_file)

            df_dict = {
                'Voltage(V)': data['voltage'],
                'Current(A)': data['current'],
                'Charge_Capacity(Ah)': data['charge_capacity'],
                'Discharge_Capacity(Ah)': data['discharge_capacity'],
                'Cycle_Index': data['cycle_index']
            }

            df = pd.DataFrame(df_dict)

            # Extracting cycles
            n_cycles = df['Cycle_Index'].max()

            for cycle in range(n_cycles):
                print(f'[🔢 {count}/{numFiles}] {cycle+1}/{n_cycles}', end='\r')
                        

                df_cycle = df.loc[df['Cycle_Index'] == cycle+1]

                df_charge, df_discharge = dqdv(df_cycle)

                # Ordering dQdV with respect to voltage
                dQdV_c = [x for _, x in sorted(
                    zip(list(df_charge['Voltage(V)']), list(df_charge['dQ/dV'])))]

                dQdV_d = [x for _, x in sorted(
                    zip(list(df_discharge['Voltage(V)']), list(df_discharge['dQ/dV'])))]

                # Constructing the DataFrame
                dfc = pd.DataFrame({
                    'Voltage(V)': df_charge['Voltage(V)'],
                    'dQ/dV': dQdV_c
                })
                dfd = pd.DataFrame({
                    'Voltage(V)': df_discharge['Voltage(V)'],
                    'dQ/dV':  dQdV_d
                })

                # Saving IDs
                dfc['id1'] = [1] * len(dQdV_c)
                dfd['id1'] = [1] * len(dQdV_d)

                dfc['id2'] = [5] * len(dQdV_c)
                dfd['id2'] = [5] * len(dQdV_d)

                if '_0_' in file:
                    id3 = 0
                elif '_1_' in file:
                    id3 = 1
                elif '_2_' in file:
                    id3 = 2
                elif '_3_' in file:
                    id3 = 3
                else:
                    id3 = 4

                dfc['id3'] = [id3] * len(dQdV_c)
                dfd['id3'] = [id3] * len(dQdV_d)

                saveName = file + '_' + str(cycle) + '.csv'

                # Saving processed data
                if len(dfc) > MIN_LENGTH:
                    dfc.to_csv(os.path.join(chargeFolder, saveName))
                if len(dfd) > MIN_LENGTH:
                    dfd.to_csv(os.path.join(dischargeFolder, saveName))

            print()

    count += 1