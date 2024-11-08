

# This file was *autogenerated* from the file data_loader.sage
from sage.all_cmdline import *   # import sage library

_sage_const_4 = Integer(4); _sage_const_3 = Integer(3); _sage_const_10 = Integer(10)
import json

with open("data/matroids.json", "r") as f:
    matroids_data = json.load(f)

with open("data/character_tables.json", "r") as g:
    character_tables = json.load(g)

j= _sage_const_4 
gdcs = []
for i in range(_sage_const_3 , _sage_const_10 ):
    key = f"U({i}, {i})"
    if key in matroids_data:
        print(key, (matroids_data[key]["gdc"]), "\n")
    else:
        print(f"No data found for U({j}, {i})")

