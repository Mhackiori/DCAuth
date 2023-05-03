# ID1: architecture (LFP = 1)
# ID2: model (APR18650M1A = 5)
# ID3: cell sample

import os
import pandas as pd
import pickle
import warnings

import sys
sys.path.insert(0, os.getcwd())

from utils.helperFunctions import *
from utils.const import *

warnings.filterwarnings("ignore")

if not sys.warnoptions:
    warnings.simplefilter("ignore")
    os.environ["PYTHONWARNINGS"] = "ignore"

step = 10

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

    if file.split('.')[1] == 'pkl' and not processed:
        # Loading file
        with open(filePath, "rb") as input_file:
            data = pickle.load(input_file)

            keys = data.keys()

            for i, key in enumerate(keys):

                cycles = data[key]['cycles']

                for j, cKey in enumerate(cycles):
                    if j%step == 0 and j != 0:
                        print(f'[🔢 FILE {count}/{numFiles}] [🔋 CELL {i+1}/{len(keys)}] [♻️  CYCLE {int(j/step)}/{int(len(cycles)/step)}]', end='\r')
                        cycle_data = cycles[cKey]

                        df_dict = {
                            'Voltage(V)': cycle_data['V'],
                            'Current(A)': cycle_data['I'],
                            'Charge_Capacity(Ah)': cycle_data['Qc'],
                            'Discharge_Capacity(Ah)': cycle_data['Qd']
                        }

                        df = pd.DataFrame(df_dict)

                        df_charge, df_discharge = dqdv(df)

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

                        dfc['id3'] = [int(key[3:])] * len(dQdV_c)
                        dfd['id3'] = [int(key[3:])] * len(dQdV_d)

                        saveName = key + '_' + cKey + '.csv'

                        # Saving processed data
                        if len(dfc) > MIN_LENGTH:
                            dfc.to_csv(os.path.join(chargeFolder, saveName))
                        if len(dfd) > MIN_LENGTH:
                            dfd.to_csv(os.path.join(dischargeFolder, saveName))

    count += 1