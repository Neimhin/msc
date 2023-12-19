import googlemaps
import json
google_maps_api_key = "AIzaSyBRuwQQKk4sx31MmBaPMefAYF79jvxewKU"

gmaps = googlemaps.Client(key=google_maps_api_key)


district_geos = []
with open("data/districts.json", 'r') as f:
    data = json.load(f)
    for district in data:
        search_string = district[0] + ", " + district[1]
        geocode_result = gmaps.geocode(search_string)
        district_geos.append({
            "district_tuple": district,
            "search_string": search_string,
            "geocode_result": geocode_result,
        })

print(json.dumps(district_geos))