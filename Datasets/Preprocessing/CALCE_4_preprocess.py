import os
import pandas as pd

cwd = os.getcwd()

for j, dir in enumerate(sorted(os.listdir(cwd))):
    if dir != 'CALCE_4' and dir != 'process.py':
        files = sorted(os.listdir(os.path.join(cwd, dir)))
        for k, file in enumerate(files):
            try:
                print(f'🔢 [{j+1}/{len(os.listdir(cwd))}] [{k+1}/{len(files)}] {file}')
                    
                # check if already processed
                if file not in os.listdir(os.path.join(cwd, 'CALCE_4')) and file.split('.')[1] in ['xls', 'xlsx']:  
                    xls = pd.ExcelFile(os.path.join(os.path.join(cwd, dir), file))
                    # Extracting and merging sheets
                    sheets = xls.sheet_names
                    idxs = []
                    for sheet in sheets:
                        if 'channel' in sheet.lower():
                            idxs.append(sheets.index(sheet))

                    dfs = []
                    for idx in idxs:
                        df = xls.parse(sheets[idx])
                        dfs.append(df)

                    filename = os.path.join(cwd, 'CALCE_4')
                    filename = os.path.join(filename, file)
                    with pd.ExcelWriter(filename) as writer:
                        for i, df in enumerate(dfs):
                            df.to_excel(writer, sheet_name=sheets[idxs[i]], index=False)
            except IndexError:
                continue