import json

chowPoly_list = []

def get_cPoly(graph):
    edgelist = graph.edges(labels = False)
    for item, cpoly in chowPoly_list:
        if  edgelist == item:
            return cpoly

    cpoly = chow_polynomial(edgelist)
    chowPoly_list.append((edgelist, cpoly))
    write_to_json(chow_data(edgelist, cpoly))

    return cpoly

def reduced_char_poly(graph):
    return graphic_char_poly(graph) // (x - 1)

def graphic_char_poly(graph):
    T = graph.tutte_polynomial()
    x = var('x')
    subbed_Tpoly = T.subs(x = 1 - x, y = 0)
    char_poly = (-1) ** Matroid(graph).rank() * subbed_Tpoly
    R = PolynomialRing(QQ, 'x')

    return R(char_poly)

def chow_polynomial(edgelist):

    M = Matroid(graph = edgelist, groundset = edgelist)
    rank = M.rank()
    x = var('x')
    R = PolynomialRing(QQ, 'x')

    if rank == 0: return R(1)
    
    chow_poly = R(0)
    
    for i in range(1, rank + 1):
        for flat in M.flats(i):
            restriction = Graph(list(flat))
            contractionGraph = Graph(edgelist)
            contractionGraph.contract_edges(list(flat))
            contraction = contractionGraph

            restriction_poly = reduced_char_poly(restriction)
            contraction_poly = R(1)

            if contraction is not None:
                contraction_poly = get_cPoly(contraction)

            term_poly = restriction_poly * contraction_poly
            
            chow_poly += term_poly
    
    return chow_poly

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
        result = chow_polynomial(edgelist)

if __name__ == "__main__":
    main()
