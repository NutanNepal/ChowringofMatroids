import json

with open("data/matroids.json", "r") as f:
    matroids_data = json.load(f)

with open("data/character_tables.json", "r") as g:
    character_tables = json.load(g)

j= 4
gdcs = []
for i in range(5, 8):
    key = f"Braid({i})"
    if key in matroids_data:
        print(key, (matroids_data[key]["dir"][1]), "\n")
    else:
        print(f"No data found for U({j}, {i})")