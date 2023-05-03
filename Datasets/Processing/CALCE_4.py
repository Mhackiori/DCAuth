# ID1: architecture (LCO = 2)
# ID2: model (CX2 = 3)
# ID3: cell sample

import os
import pandas as pd
import warnings

import sys
sys.path.insert(0, os.getcwd())

from utils.const import *
from utils.helperFunctions import *


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

    if file.split('.')[1] == 'xls' or file.split('.')[1] == 'xlsx' and not processed:
        try:
            # Loading file
            xls = pd.ExcelFile(filePath)

            # Extracting and merging sheets
            sheets = xls.sheet_names
            df = xls.parse(sheets[0])
            if len(sheets) > 1:
                for sheet in sheets:
                    # Removing last element since it's replicated in next sheet
                    df = df.iloc[:-1, :]
                    try:
                        df = df.merge(xls.parse(sheet))
                    except:
                        continue

            # Extracting cycles
            n_cycles = df['Cycle_Index'].max()

            if type(n_cycles) != float:
                for cycle in range(n_cycles):
                    saveName = file.split('.')[0] + '_' + str(cycle) + '.csv'

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
                    dfc['id1'] = [2] * len(dQdV_c)
                    dfd['id1'] = [2] * len(dQdV_d)

                    dfc['id2'] = [3] * len(dQdV_c)
                    dfd['id2'] = [3] * len(dQdV_d)

                    dfc['id3'] = [file.split('_')[1]] * len(dQdV_c)
                    dfd['id3'] = [file.split('_')[1]] * len(dQdV_d)

                    # Saving processed data
                    if len(dfc) > MIN_LENGTH:
                        dfc.to_csv(os.path.join(chargeFolder, saveName))
                    if len(dfd) > MIN_LENGTH:
                        dfd.to_csv(os.path.join(dischargeFolder, saveName))
        except KeyError:
            continue

    count += 1

print()
