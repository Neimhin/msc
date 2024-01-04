import pandas as pd
import os
import numpy as np
import sys
source_file = sys.argv[1]
data = pd.read_csv(source_file)
data['TIME'] = pd.to_datetime(data['TIME'], format='%Y-%m-%d %H:%M:%S')
directory = source_file + ".d"
os.makedirs(directory, exist_ok=True)
data['TIME DIFF'] = data.groupby('STATION ID')['TIME'].diff().dt.total_seconds() / 60
data['MISSING SAMPLES'] = data['TIME DIFF'].apply(lambda x: np.round((x - 5) / 5) if x >= 6 else 0)
result = data.groupby([data['TIME'].dt.year, 'NAME'])['MISSING SAMPLES'].sum().unstack(fill_value=0)
result.to_csv(f"{directory}/missing_samples_by_station_year.csv")


data.groupby([data['TIME'].dt.month, 'NAME'])['MISSING SAMPLES'].sum().unstack(fill_value=0).to_csv(f"{directory}/missang_samples_by_station_month.csv")
data.groupby([data['TIME'].dt.date,  'NAME'])['MISSING SAMPLES'].sum().unstack(fill_value=0).to_csv(f"{directory}/missang_samples_by_station_date.csv")
