from utilities import *
import numpy as np
import pandas as pd

analysis_folder = "Analytics/Results/"
global_statistics_folder = f"{analysis_folder}GlobalStatistics/"
files = sorted(list_files_in_directory(analysis_folder), key=lambda name: int(name.split('.')[0]))

columns = [
    "Минимальная разница",
    "Максимальная разница",
    "Средняя разница",
    "Средняя абсолютная разница",
    "Медиана разницы рассчитанной и реальной глубины",
    "Медиана абсолютной разницы",
    "Cреднеквадратичное отклонение",
    "Cреднее абсолютное отклонение MAD",
    "Процент дальних пикселей на SGBM",
    "Процент дальних пикселей из движка",
    "Процент ложно-отрицательных дальних пикселей",
    "Процент ложно-положительных дальних пикселей",
]
print(len(columns))

dataset = pd.DataFrame(columns=columns)
for filename in files:
    with open(f"{analysis_folder}{filename}", "r", encoding='utf-8') as f:
        data = list(map(float, f.readline().split()))
    # print(len(data))

    dataset.loc[len(dataset.index)] = data

print(dataset.describe())
dataset.to_csv(f"{global_statistics_folder}final_global_analysis.csv")

for column in columns:
    print('-'*50)
    print(dataset[column].describe())
