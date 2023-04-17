import numpy as np
import os
import pandas as pd
import sys
import warnings
warnings.filterwarnings("ignore")

if not sys.warnoptions:
    warnings.simplefilter("ignore")
    os.environ["PYTHONWARNINGS"] = "ignore"

df = pd.read_csv('./EIL-MJ1-015.csv')

dfs = [
    df[df.columns[5:10]],
    df[df.columns[11:16]],
    df[df.columns[17:22]],
    df[df.columns[23:28]],
    df[df.columns[29:35]]
]

dfs2 = []

for i, this_df in enumerate(dfs):
    this_df.rename(columns = {this_df.columns[0]: this_df.columns[0].split('.')[0],
                                    this_df.columns[1]: this_df.columns[1].split('.')[0],
                                    this_df.columns[2]: this_df.columns[2].split('.')[0],
                                    this_df.columns[3]: this_df.columns[3].split('.')[0],
                                    this_df.columns[4]: this_df.columns[4].split('.')[0]
                                    }, inplace = True)

    this_df = this_df.drop(['Test Time', 'Temp'], axis=1)
    this_df.replace('', np.nan, inplace=True)
    this_df.dropna(subset=['Cycle Number'], inplace=True)
    this_df['Cycle Number'] = this_df['Cycle Number'].astype(int)

    current = []
    for cycle in this_df['Cycle Number'].unique():
        cycle_df = this_df[this_df['Cycle Number'] == cycle]
        cycle_current = []
        for v in (cycle_df['Cell Potential']):
            if v <= 4.19 and 0 not in cycle_current:
                cycle_current.append(1.5)
                current.append(1.5)
            elif v > 4.19 and -4 not in cycle_current:
                cycle_current.append(0)
                current.append(0)
            else:
                cycle_current.append(-4)
                current.append(-4)

    this_df['Current'] = current

    dfs2.append(this_df)

df_tot = pd.concat(dfs2)
df_tot.to_csv('./UCL.csv', index=False)