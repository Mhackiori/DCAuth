# ID1: architecture
    # NMC = 0
    # LFP = 1
    # LCO = 2
    # NCA = 3
# ID2: model
    # A123 APR18650M1 = 1
    # NCR18650B = 5
    # 18650HG2 = 6
    # SLPB533459H4 = 7
    # ICR18650 C2 = 8
# ID3: cycling

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

subsets = ['HNEI', 'OX', 'SNL', 'UL']

for subset in subsets:
    processedFolder = os.path.join(
        './Datasets/Processed/', subset)
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

        if file.split('.')[-1] == 'csv' and subset in file and not processed:
            df = pd.read_csv(filePath)

            # Extracting cycles
            n_cycles = int(df['Cycle_Index'].max())

            for cycle in range(n_cycles):
                print(f'[🔢 {count}/{numFiles}] {cycle}/{n_cycles}', end='\r')
                saveName = file.split('.')[0] + '_' + str(cycle) + '.csv'

                df_cycle = df.loc[df['Cycle_Index'] == cycle+1]

                df_charge, df_discharge = dqdv(df_cycle, equip='Arbin_BA')

                # Ordering dQdV with respect to voltage
                dQdV_c = [x for _, x in sorted(
                    zip(list(df_charge['Voltage (V)']), list(df_charge['dQ/dV'])))]

                dQdV_d = [x for _, x in sorted(
                    zip(list(df_discharge['Voltage (V)']), list(df_discharge['dQ/dV'])))]

                # Constructing the DataFrame
                dfc = pd.DataFrame({
                    'Voltage(V)': df_charge['Voltage (V)'],
                    'dQ/dV': dQdV_c
                })
                dfd = pd.DataFrame({
                    'Voltage(V)': df_discharge['Voltage (V)'],
                    'dQ/dV':  dQdV_d
                })

                # Saving IDs
                if subset != 'HNEI':
                    if 'NMC' in file:
                        id1 = 0
                    elif 'LFP' in file:
                        id1 = 1
                    elif 'LCO' in file:
                        id1 = 2
                    else:
                        id1 = 3
                else:
                    id1 = 4

                dfc['id1'] = [id1] * len(dQdV_c)
                dfd['id1'] = [id1] * len(dQdV_d)

                if id1 == 1:
                    id2 = 1
                elif id1 == 0:
                    id2 = 6
                elif id1 == 2:
                    id2 = 7
                elif id1 == 3:
                    id2 = 5
                else:
                    id2 = 8


                dfc['id2'] = [id2] * len(dQdV_c)
                dfd['id2'] = [id2] * len(dQdV_d)

                dfc['id3'] = [str(cycle)] * len(dQdV_c)
                dfd['id3'] = [str(cycle)] * len(dQdV_d)

                # Saving processed data
                if len(dfc) > MIN_LENGTH:
                    dfc.to_csv(os.path.join(chargeFolder, saveName))
                if len(dfd) > MIN_LENGTH:
                    dfd.to_csv(os.path.join(dischargeFolder, saveName))

        count += 1