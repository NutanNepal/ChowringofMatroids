class MMPR21:

    def __init__(self):
        self.base_ring = PolynomialRing(QQ, 'x')
        self.x = self.base_ring.gens()[0]
        Sym = SymmetricFunctions(self.base_ring)
        Sym.inject_shorthands()
        self.name = "fixed"
        self.memoize_B = {}
        self.memoize_A = {}
        self.chowPoly_list = []

    def lieN(self, n):
        """
        Return the symmetric function `\\ell_n`, which is the
        Frobenius image of `\\mathrm{Lie}_{(n)}` in [HR17].
        """
        div = divisors(n)
        return (1/n)*sum(moebius(d)*p[d]^(n//d) for d in div)

    def wLambda(self, lamb):
        """
        Return the symmetric function 
        `\\mathrm{ch}(\\mathrm{W}_{\\lambda})` from [HR17].
        """
        expPartition = lamb.to_exp()
        return prod(h[expPartition[i]](
            self.lieN(i+1).omega()) for i in range(0,len(expPartition))[::2])*prod(e[expPartition[i]](
                self.lieN(i+1).omega()) for i in range(1,len(expPartition))[::2])

    def rankOfPartition(self, lamb):
        """
        Return the rank of a partition `\\lambda` as in [HR17, Definition 2.5].
        """
        expPartition = lamb.to_exp()
        return sum(i*expPartition[i] for i in range(0,len(expPartition)))

    def A(self, n, i):
        """
        Return the symmetric function corresponding to the 
        `\\mathfrak{S}_n`-representation `A_n^i` from [MMPR21].
        """
        if (n,i) not in self.memoize_A:
            ourPartitions = []
            for k in Partitions(n):
                if self.rankOfPartition(k) == i:
                    ourPartitions.append(k)
            self.memoize_A[(n,i)] = sum(self.wLambda(lamb) for lamb in ourPartitions)
        return self.memoize_A[(n,i)]

    def qA(self, n):
        """
        Return the symmetric function, with `q`-coefficients,
        corresponding to the graded
        `\\mathfrak{S}_n`-representation `A_n` from [MMPR21].
        """
        return sum(self.A(n,j) * self.x**j for j in range(n))

    def B(self, n, i):
        """
        Return the symmetric function corresponding to the 
        `\\mathfrak{S}_n`-representation `B_n^i` from [MMPR21].
        """
        if (n,i) not in self.memoize_B:
            if n == 1:
                print('do not give me n = 1')
            if i == 0:
                self.memoize_B[(n,i)] = s([n])
            else:
                self.memoize_B[(n,i)] = self.A(n,i) - self.B(n,i-1)
        return self.memoize_B[(n,i)]

    def qB(self, n):
        """
        Return the symmetric function, with `q`-coefficients,
        corresponding to the graded
        `\\mathfrak{S}_n`-representation `B_n` from [MMPR21].
        """
        return sum(self.B(n,j) * self.x**j for j in range(n))

class Matroids:

    def __init__(self, name, permutationGroup, interface):
        self.name = name
        self.permutationGroup = permutationGroup
        self.mmpr = interface

    # x, y are symmetric functions
    def iTensor(x, y):
        return x.itensor(y)
    
    # x is a partition
    def induced_representation_step(x):
        y = []
        for j in range(len(x) + 1):
            y.append(x.add_cell(j))
        
        return y
    
    def induced_representation(x, m, n)
        y = induced_representation_step(x)
        if n - m > 1:
            y.append(induced_representation(y, m + 1, n)
        return y

    def reduced_osg(x):
        # to-do
        return 1

    def get_cPoly(self, M):
        for item, cpoly in self.chowPoly_list:
            if  M.is_isomorphic(item):
                return cpoly
        
        cpoly = equiv_chow(M)
        self.chowPoly_list.append((M, cpoly))

        return cpoly

    def equiv_chow(self, matroid):
        rank = M.rank()
        if rank == 0: return self.base_ring(1)

        chow_poly = self.base_ring(0)

        for i in range(1, rank + 1):
            for flat in M.flats(i):
                restriction = M.delete(M.groundset() - flat).simplify()
                contraction = M.contract(flat).simplify()
                
                restriction_poly = reduced_osg(restriction)
                contraction_poly = self.get_cPoly(contraction)
                
                term_poly = self.iTensor(restriction_poly, contraction_poly)
                
                chow_poly += term_poly
        

