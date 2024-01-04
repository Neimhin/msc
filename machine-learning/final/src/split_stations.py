import pandas as pd
import os
import sys
infile = sys.argv[1]
outdir = sys.argv[2]
data = pd.read_csv(infile)
data['TIME'] = pd.to_datetime(data['TIME'], format='%Y-%m-%d %H:%M:%S')
os.makedirs(outdir, exist_ok=True)
for station_id in data['STATION ID'].unique():
    station_data = data[data['STATION ID'] == station_id]
    station_name = station_data['NAME'].iloc[0]
    print(station_id, station_name, len(station_data["NAME"].unique()))
    station_data = station_data.sort_values(by='TIME')
    filename = f"{station_id}-{station_name}.csv".replace("/", "-").replace(" ", "_")
    station_data.to_csv(f'{outdir}/{filename}', index=False)
