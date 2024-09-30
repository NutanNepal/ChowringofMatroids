import json

with open("data/matroids.json", "r") as f:
    matroids_data = json.load(f)

with open("data/character_tables.json", "r") as g:
    character_tables = json.load(g)

j= 3
gdcs = []
for i in range(3, 10):
    key = f"U({j}, {i})"
    if key in matroids_data:
        print((matroids_data[key]["gdc"]))
    else:
        print(f"No data found for U({j}, {i})")

print(character_tables["4"])