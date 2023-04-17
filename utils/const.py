import os

# Seed for reproducibility
SEED = 151836

# Folders
RAW = './Datasets/Raw/'
PROCESSED = './Datasets/Processed/'

# Datasets
# DATASETS = [
#     'Berkley',
#     'CALCE_1',
#     'CALCE_2',
#     'CALCE_3',
#     'CALCE_4',
#     'CALCE_5',
#     'EVERLASTING_1',
#     'EVERLASTING_2',
#     'HNEI',
#     'OX',
#     'OX_1',
#     'OX_2',
#     'SNL',
#     'TRI_1',
#     # 'TRI_2',
#     'UCL',
#     'UL'
# ]
DATASETS = sorted(os.listdir(PROCESSED))

MIN_LENGTH = 90