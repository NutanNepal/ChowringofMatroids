import chowpoly_graphical.sage

def chow_data(edgelist, poly):
    serialized_matroid = {
        "name": list(edgelist),
        "chow_polynomial": str(poly)
    }
    return serialized_matroid

def write_to_json(chow_data):
    with open("chowpolys.json", "a") as f:
        json.dump(chow_data, f)
        f.write("\n")

def main():
    for i in range(3, 20):
        edgelist = graphs.CompleteGraph(i).edges(labels = False)
        result = chowpoly_graphical.chow_polynomial(edgelist)

if __name__ == "__main__":
    main()