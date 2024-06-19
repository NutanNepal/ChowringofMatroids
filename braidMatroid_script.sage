import numpy as np
import json
import sys

class Matroids:

    def __init__(self, name, symmetric_group_n):
        self.name = name
        self.symmetric_group_n = symmetric_group_n
        self.rank = self.name.rank()
        self.conjugacy_Classes, self.class_actions = self.generate_conjugacyClasses(
            self.symmetric_group_n
        )
        weights = generate_weights(self.rank)
        maxChains = self.maximalChains(self.name.lattice_of_flats())
        self.fy_monomials = self.generate_fyMonomials(maxChains, weights)
        self.representation_polynomial = self.representation_polynomial()
        self.dimensions = self.dimensions(self.fy_monomials)
        self.trace_matrix = self.representations(self.symmetric_group_n)

    def maximalChains(self, lattice_of_flats):
        return [
            [list(chain) for chain in p][1:]
            for p in list(lattice_of_flats.chains()) if len(p) == self.rank + 1
        ]

    def representation_polynomial(self):
        characters_list_graded = self.characters_list(self.fy_monomials, self.class_actions)
        representation_polynomial = self.decomposition(
            characters_list_graded, self.symmetric_group_n)
        return representation_polynomial


    def generate_fyMonomials(self, maxChains, weights):
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
    
    def generate_conjugacyClasses(self, n):
        def subdivide_set(partition_set):
            partitions = []
            elements = list(range(n))
            for length in partition_set:
                partition = elements[:length]
                partitions.append(partition)
                for i in range(length):
                    elements.pop(0)
            return partitions

        conjugacy_classes = Partitions(n).list()
        subdivided_partitions = [subdivide_set(part) for part in conjugacy_classes]

        class_actions = []
        for partition in subdivided_partitions:
            irr_representation = {}
            for x in partition:
                for i, element in enumerate(x):
                    irr_representation[element] = x[(i + 1) % len(x)]
            class_actions.append(irr_representation)
            
        return conjugacy_classes, class_actions
    
    def mutable_fyMonomials(self, fy_monomials):
        mutable_fyMonomials = []
        for graded_piece in fy_monomials:
            mutable_graded_piece = [list(monomial) for monomial in graded_piece]
            mutable_fyMonomials.append(mutable_graded_piece)

        return mutable_fyMonomials

    def apply_map(self, monomial, mapping):
        mapped_monomial = []
        for term in monomial:
            new_term = []
            for edge in term[0]:
                new_edge = tuple(sorted([mapping[int(x)] for x in edge]))
                new_term.append(new_edge)
            mapped_monomial.append(tuple((tuple(new_term), term[1])))
        return tuple(sorted(mapped_monomial))

    def monomial_equality(self, monomial, mapped_monomial):
        #sorting the inner tuples, and outer tuples and so on and on

        sorted_monomial = [(sorted(
            [tuple(sorted(segment)) for segment in m[0]]), m[1]
                                    ) for m in monomial]
        sorted_mapped_monomial = [(sorted(
            [tuple(sorted(segment)) for segment in m[0]]), m[1]
                                    ) for m in mapped_monomial]
        sorted_monomial.sort()
        sorted_mapped_monomial.sort()

        for i in range(len(sorted_monomial)):
            if sorted_monomial[i] != sorted_mapped_monomial[i]:
                return False

        return True

    def character(self, temp_fyMonomials, irr_representation):
        i = 0
        for monomial in temp_fyMonomials:
            mapped_monomial = tuple(sorted(
                self.apply_map(monomial, irr_representation)
                ))
            if self.monomial_equality(monomial, mapped_monomial): i += 1
        return i

    def characters_list(self, fy_monomials, class_actions):
        mutable_fyMonomialsList = self.mutable_fyMonomials(fy_monomials)
        characters_list = []
        for i in range(len(mutable_fyMonomialsList)):
            characters_list.append(
                [self.character(
                    mutable_fyMonomialsList[i], mapping) for mapping in class_actions]
            )
        return characters_list
    
    def representations(self, n):
        representations = []
        partitions = Partitions(n).list()
        for partition in partitions:
            character_values = SymmetricGroupRepresentation(partition).to_character().values()
            int_values = [int(value) for value in character_values]
            representations.append(int_values)
        return representations


    def decomposition(self, characters_list, n):
        # solving the equation Ax = b.
        trace_matrix = np.matrix(self.representations(n), dtype=float)
        decomposition = []
        A = np.array(trace_matrix.transpose())
        for v in characters_list:
            v.reverse()
            rhs_array = np.array(v, dtype=float)
            solution = np.linalg.solve(A, rhs_array)
            rounded_solution = np.round(solution).astype(int)
            decomposition.append(rounded_solution.tolist())

        return decomposition
    
    def dimensions(self, fy_monomials):
        dimensions = [0] * len(fy_monomials)
        for i in range(len(fy_monomials)):
            dimensions[i] = len(fy_monomials[i])
        return dimensions

def generate_weights(rank):
    weights = set() 
    for i in range(1, rank):
        for j in range(rank):
            weight = [0] * rank
            if i >= j:
                weight[i] = j
                weights.add(tuple(weight))
            if rank - (i+1) > 1:
                y = generate_weights(rank - (i + 1))  # Recursion
                for x in y:
                    temp_weight = weight.copy()
                    weights.add(tuple(temp_weight[:i+1] + x)) 

    return [list(w) for w in weights]

def create_matroid(i):
    matroid = Matroids(Matroid(graphs.CompleteGraph(i)), i)
    serialized_matroid = {
        "name": str(matroid.name),
        "rank": matroid.rank,
        "sn": int(matroid.symmetric_group_n),
        "gdc": matroid.dimensions,
        "dir": matroid.representation_polynomial
    }
    return serialized_matroid

def write_to_json(matroid_data):
    with open("braidMatroids.json", "a") as f:
        json.dump(matroid_data, f)
        f.write("\n")

def main():
    print(len(sys.argv))
    if len(sys.argv) != 2:
        print("Usage: python script.py i")
        sys.exit(1)

    i = int(sys.argv[1])

    matroid_data = create_matroid(i)
    write_to_json(matroid_data)

if __name__ == "__main__":
    main()