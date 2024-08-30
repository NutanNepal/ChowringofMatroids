#returns if there is a graph isomorphism between two graphs.
#is a little faster than the stock function.

def is_graphisomorphism(g1, g2):
    g1_edges = g1.edges(labels = False)
    g2_edges = g2.edges(labels = False)

    def reduceGroup(g):
        distinct = set()
        for t in g:
            for e in t:
                distinct.add(e)
        
        d = {}
        s = sorted(distinct)
        for idx, x in enumerate(s):
            d[x] = idx
        
        l = []
        for t in g:
            tup = []
            for e in t:
                tup.append(d[e])
            l.append(tuple(tup))

        return sorted(l)

    return reduceGroup(g1_edges) == reduceGroup(g2_edges)

