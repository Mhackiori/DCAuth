import scipy.io
import pandas as pd

mat = scipy.io.loadmat('./Oxford_Battery_Degradation_Dataset_1.mat')

for i in range(1, 9):
    key = 'Cell' + str(i)
    # print(key)
    dfs_c = []
    dfs_d = []
    for j, cycle_data in enumerate(mat[key][0][0]):
        print(f'[{i}/8] {j+1}/{len(mat[key][0][0])}')
        cycle_number = str(j+1)
        for k, cd in enumerate(cycle_data[0][0]):
            if k == 0 or k == 1:  # charge or discharge
                data = cd[0][0]
                voltage = list([x[0] for x in data[1]])
                charge = list([x[0] for x in data[2]])
                cycle_index = list([j+1] * len(voltage))
                if k == 0:
                    df_dict = {
                        'Voltage(V)': voltage,
                        'Charge_Capacity(Ah)': charge,
                        'Cycle_Index': cycle_index
                    }
                    df = pd.DataFrame(df_dict)
                    dfs_c.append(df)
                if k == 1:
                    df_dict = {
                        'Voltage(V)': voltage,
                        'Discharge_Capacity(Ah)': charge,
                        'Cycle_Index': cycle_index
                    }
                    df = pd.DataFrame(df_dict)
                    dfs_d.append(df)
    
    dfc = pd.concat(dfs_c)
    dfd = pd.concat(dfs_d)

    cName = './OX_' + key + '_Charge.csv'
    dName = './OX_' + key + '_Discharge.csv'
    dfc.to_csv(cName)
    dfd.to_csv(dName)