# The Matroid Class

The Matroid class has the following properties:

    1. name : (string) Name of the matroid, as provided by sagemath,
    2. rank : (integer) the rank of the matroid,
    3. sn : (integer) an integer 'n' that corresponds to the symmetric group S_n that acts on the matroid,
    4. ct : (list of lists of integers) the character table for the symmetric group S_n,
    5. gdc : (list of integers) (graded dimensions Chow) the dimensions of the graded pieces of the Chow ring,
    6. dir : (list of lists of integers) (decomposition into irreducibles) decomposition of each graded piece into irreducible representations.
