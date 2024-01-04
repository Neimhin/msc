import pandas as pd
import os
import lib
import numpy as np
import sys

main_file = sys.argv[1]
data = pd.read_csv(main_file)
data['TIME'] = lib.to_datetime(data['TIME'])
os.makedirs('data/station', exist_ok=True)

def calculate_and_sort_missing_intervals(station_data):
    station_data = station_data.sort_values(by='TIME')
    station_data["TIME DIFF"] = station_data["TIME"].diff().dt.total_seconds() / 60
    missing_data_mask = station_data["TIME DIFF"] > 6
    missing_intervals = station_data.loc[missing_data_mask, ["TIME", "TIME DIFF"]]
    missing_intervals["START TIME"] = missing_intervals["TIME"] - pd.to_timedelta(missing_intervals["TIME DIFF"], unit='m')
    missing_intervals["END TIME"] = missing_intervals["TIME"]
    missing_intervals["INTERVAL LENGTH"] = missing_intervals["TIME DIFF"]
    missing_intervals = missing_intervals.sort_values(by="INTERVAL LENGTH", ascending=False)
    return missing_intervals[["START TIME", "END TIME", "INTERVAL LENGTH"]]


for station_id in data['STATION ID'].unique():
    station_data = data[data['STATION ID'] == station_id]
    station_name = station_data['NAME'].iloc[0]
    print(station_id, station_name, len(station_data["NAME"].unique()))
    station_data = station_data.sort_values(by='TIME')
    station_data["TIME DIFF"] = station_data["TIME"].diff().dt.total_seconds() / 60
    missing_data_mask = station_data["TIME DIFF"] >= 6 # minutes
    total_missing_time = station_data.loc[missing_data_mask, "TIME DIFF"].sum()
    station_data['MISSING SAMPLES'] = station_data.loc[missing_data_mask, "TIME DIFF"].apply(lambda x: np.round((x - 5) / 5))
    total_missing_samples = station_data["MISSING SAMPLES"].sum()
    filename = f"{station_id}-{station_name}.csv".replace("/", "-").replace(" ", "_")
    directory = f"{main_file}.d/{filename}.d"
    os.makedirs(directory,exist_ok=True)

    missing_intervals = calculate_and_sort_missing_intervals(station_data)
    missing_intervals.to_csv(directory + "/missing-intervals.csv")

    with open(directory + "/missing-data.txt","w") as f:
        lib.tee(station_id, station_name,file=f)
        lib.tee("missing time:", (total_missing_time / 60) /24, "days", file=f)
        lib.tee("missing samples:", total_missing_samples, file=f)
