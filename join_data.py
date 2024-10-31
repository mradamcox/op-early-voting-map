import json
import csv

with open("Voting Precincts_20241031.geojson", "r") as o:
    geojson = json.load(o)
print(f"{len(geojson['features'])} precinct geometries")

lookup = {}
with open("2024-11-05 Early Voting_Orleans Parish_Table.csv", "r") as o:
    reader = csv.DictReader(o)
    for row in reader:
        lookup[row["Parish Ward Precinct"]] = row
print(f"{len(lookup)} precincts in voting data")



for f in geojson['features']:

    w, p = f['properties']['precinctid'].split("-")

    # handle single digit precinct with suffixed ones that don't zfill(2) well
    if len(p) == 2 and p[-1] in ["A", "B", "C"]:
        p = "0" + p

    title = f"PAR 36 W {w.zfill(2)} P {p.zfill(2)}"
    if not title in lookup:
        continue

    row = lookup[title]
    f['properties'].update({
        "title": title,
        "registered_voters": int(row["Registered Voters (as of 10/1/24)"]),
        "yet_to_vote": int(row["Yet to Vote"]),
        "ev_turnout": float(row["%EV Turnout"]),
    })

with open("Voting Precincts_20241031-with-early-voting-data.geojson", "w") as o:
    json.dump(geojson, o, indent=2)
