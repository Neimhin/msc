import sys
import pandas as pd
import json
df = pd.read_csv(sys.argv[1])

places = []
for i,r in df.iterrows():
    places.append((r["event_location_district"], r["event_location_region"]))
places = list(set(places))
print(len(places))
print(json.dumps(places))