n = 7
G = graphs.CompleteGraph(n)
B = Matroid(G)
L = B.lattice_of_flats()

frozenChains = list(L.chains())

maxChains = [[list(chain) for chain in p][1:] for p in frozenChains if len(p) == B.rank() + 1]
print("number of maximal chains: ", len(maxChains))

def generate_weights(rank):
    weights = set() 
    for i in range(1, rank):
        for j in range(rank):
            weight = [0] * rank
            
            if i >= j:
                weight[i] = j
                weights.add(tuple(weight))

            if rank - (i+1) > 1:
                y = generate_weights(rank - (i + 1))  # Recursion to get the complete list of weights...
                for x in y:
                    temp_weight = weight.copy()
                    weights.add(tuple(temp_weight[:i+1] + x)) 

    return [list(w) for w in weights]

rank = n-1
all_weights = generate_weights(rank)

def generate_fyMonomials(maxChains, weights):
    fy_monomials = [set() for _ in range(len(weights[0]))]
    for chain in maxChains:
        for weight in weights:
            degree = sum(weight)
            fy_monomial = []
            for i, segment in enumerate(chain):
                if weight[i] > 0:
                    fy_monomial.append((tuple(segment), weight[i]))
            fy_monomials[degree].add(frozenset(fy_monomial))
    return fy_monomials

fy_monomials = generate_fyMonomials(maxChains, all_weights)

dimensions = [0] * rank
for i in range(rank):
    dimensions[i] = len(fy_monomials[i])
print("dimensions of graded pieces : ", dimensions)

def generate_conjugacyClasses(n):
    def partition(n, m=None):
        if m is None:
            m = n
        if n == 0:
            return [[]]
        if n < 0 or m == 0:
            return []
        partitions = partition(n, m - 1)
        partitions.extend([sublist + [m] for sublist in partition(n - m, m)])
        return partitions

    def subdivide_set(partition_set):
        partitions = []
        elements = list(range(n))
        for length in partition_set:
            partition = elements[:length]
            partitions.append(partition)
            for i in range(length):
                elements.pop(0)
        return partitions

    partitions = partition(n)
    subdivided_partitions = [subdivide_set(part) for part in partitions]

    conjugacy_classes = []
    for partition in subdivided_partitions:
        conjugacy_class = {}
        for x in partition:
            for i, element in enumerate(x):
                conjugacy_class[element] = x[(i + 1) % len(x)]
        conjugacy_classes.append(conjugacy_class)
        
    return conjugacy_classes, partitions

conjugacy_Classes, irreducible_Representations = generate_conjugacyClasses(n)
print("conjugacy classes/ irreducible reps :", irreducible_Representations)

mutable_fyMonomials = []
for graded_piece in fy_monomials:
    mutable_graded_piece = [list(monomial) for monomial in graded_piece]
    mutable_fyMonomials.append(mutable_graded_piece)
    
def apply_map(monomial, mapping):
    mapped_monomial = []
    for term in monomial:
        new_term = []
        for edge in term[0]:
            new_edge = tuple(sorted([mapping[int(x)] for x in edge]))
            new_term.append(new_edge)
        mapped_monomial.append(tuple((tuple(new_term), term[1])))
    return tuple(sorted(mapped_monomial))

def monomial_equality(monomial, mapped_monomial):
    #sorting the inner tuples, and outer tuples and so on and on
    sorted_monomial = [(sorted([tuple(sorted(segment)) for segment in m[0]]), m[1]) for m in monomial]
    sorted_mapped_monomial = [(sorted([tuple(sorted(segment)) for segment in m[0]]), m[1]) for m in mapped_monomial]
    sorted_monomial.sort()
    sorted_mapped_monomial.sort()

    for i in range(len(sorted_monomial)):
        if sorted_monomial[i] != sorted_mapped_monomial[i]:
            return False

    return True

def character(temp_fyMonomials, conjugacy_Class):
    i = 0
    for monomial in temp_fyMonomials:
        mapped_monomial = tuple(sorted(apply_map(monomial, conjugacy_Class)))
        if monomial_equality(monomial, mapped_monomial): i += 1
    return i


characters = [character(mutable_fyMonomials[1], mapping) for mapping in conjugacy_Classes]
print("characters : ", characters)
