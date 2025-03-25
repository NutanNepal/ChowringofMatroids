class QuantumMoebiusAlgebra(Parent, UniqueRepresentation):
    r"""
    The quantum Möbius algebra of a lattice.

    Let `L` be a lattice, and we define the *quantum Möbius algebra* `M_L(q)`
    as the algebra with basis `\{ E_x \mid x \in L \}` with
    multiplication given by

    .. MATH::

        E_x E_y = \sum_{z \geq a \geq x \vee y} \mu_L(a, z)
        q^{\operatorname{crk} a} E_z,

    where `\mu_L` is the Möbius function of `L` and `\operatorname{crk}`
    is the corank function (i.e., `\operatorname{crk} a =
    \operatorname{rank} L - \operatorname{rank}` a). At `q = 1`, this
    reduces to the multiplication formula originally given by Solomon.
    """
    def __init__(self, L, q=None) -> None:
        """
        Initialize ``self``.

        TESTS::

            sage: L = posets.BooleanLattice(4)
            sage: M = L.quantum_moebius_algebra()
            sage: TestSuite(M).run() # long time

            sage: from sage.combinat.posets.moebius_algebra import QuantumMoebiusAlgebra
            sage: L = posets.Crown(2)
            sage: QuantumMoebiusAlgebra(L)
            Traceback (most recent call last):
            ...
            ValueError: L must be a lattice
        """
        if not L.is_lattice():
            raise ValueError("L must be a lattice")
        if q is None:
            q = LaurentPolynomialRing(ZZ, 'q').gen()
        self._q = q
        R = q.parent()
        cat = Algebras(R).WithBasis()
        if L in FiniteEnumeratedSets():
            cat = cat.Commutative().FiniteDimensional()
        self._lattice = L
        self._category = cat
        Parent.__init__(self, base=R, category=self._category.WithRealizations())

    def _repr_(self):
        """
        Return a string representation of ``self``.

        EXAMPLES::

            sage: L = posets.BooleanLattice(4)
            sage: L.quantum_moebius_algebra()
            Quantum Moebius algebra of Finite lattice containing 16 elements
             with q=q over Univariate Laurent Polynomial Ring in q over Integer Ring
        """
        txt = "Quantum Moebius algebra of {} with q={} over {}"
        return txt.format(self._lattice, self._q, self.base_ring())

    def a_realization(self):
        r"""
        Return a particular realization of ``self`` (the `B`-basis).

        EXAMPLES::

            sage: L = posets.BooleanLattice(4)
            sage: M = L.quantum_moebius_algebra()
            sage: M.a_realization()
            Quantum Moebius algebra of Finite lattice containing 16 elements
             with q=q over Univariate Laurent Polynomial Ring in q
             over Integer Ring in the natural basis
        """
        return self.E()

    def lattice(self):
        """
        Return the defining lattice of ``self``.

        EXAMPLES::

            sage: L = posets.BooleanLattice(4)
            sage: M = L.quantum_moebius_algebra()
            sage: M.lattice()
            Finite lattice containing 16 elements
            sage: M.lattice() == L
            True
        """
        return self._lattice

    class E(BasisAbstract):
        r"""
        The natural basis of a quantum Möbius algebra.

        Let `E_x` and `E_y` be basis elements of `M_L` for some lattice `L`.
        Multiplication is given by

        .. MATH::

            E_x E_y = \sum_{z \geq a \geq x \vee y} \mu_L(a, z)
            q^{\operatorname{crk} a} E_z,

        where `\mu_L` is the Möbius function of `L` and `\operatorname{crk}`
        is the corank function (i.e., `\operatorname{crk} a =
        \operatorname{rank} L - \operatorname{rank}` a).
        """
        def __init__(self, M, prefix='E') -> None:
            """
            Initialize ``self``.

            TESTS::

                sage: L = posets.BooleanLattice(4)
                sage: M = L.quantum_moebius_algebra()
                sage: TestSuite(M.E()).run() # long time
            """
            self._basis_name = "natural"
            CombinatorialFreeModule.__init__(self, M.base_ring(),
                                             tuple(M._lattice),
                                             prefix=prefix,
                                             category=MoebiusAlgebraBases(M))

        def product_on_basis(self, x, y):
            """
            Return the product of basis elements indexed by ``x`` and ``y``.

            EXAMPLES::

                sage: L = posets.BooleanLattice(4)
                sage: E = L.quantum_moebius_algebra().E()
                sage: E.product_on_basis(5, 14)
                E[15]
                sage: E.product_on_basis(2, 8)
                q^2*E[10] + (q-q^2)*E[11] + (q-q^2)*E[14] + (1-2*q+q^2)*E[15]
            """
            L = self.realization_of()._lattice
            q = self.realization_of()._q
            moebius = L.moebius_function
            rank = L.rank_function()
            R = L.rank()
            j = L.join(x, y)
            return self.sum_of_terms((z, moebius(a, z) * q**(R - rank(a)))
                                     for z in L.order_filter([j])
                                     for a in L.closed_interval(j, z))

        @cached_method
        def one(self):
            """
            Return the element ``1`` of ``self``.

            EXAMPLES::

                sage: L = posets.BooleanLattice(4)
                sage: E = L.quantum_moebius_algebra().E()
                sage: all(E.one() * b == b for b in E.basis())
                True
            """
            L = self.realization_of()._lattice
            q = self.realization_of()._q
            moebius = L.moebius_function
            rank = L.rank_function()
            R = L.rank()
            return self.sum_of_terms((x, moebius(y, x) * q**(rank(y) - R))
                                     for x in L for y in L.order_ideal([x]))

    natural = E

    class C(BasisAbstract):
        r"""
        The characteristic basis of a quantum Möbius algebra.

        The characteristic basis `\{ C_x \mid x \in L \}` of `M_L`
        for some lattice `L` is defined by

        .. MATH::

            C_x = \sum_{a \geq x} P(F^x; q) E_a,

        where `F^x = \{ y \in L \mid y \geq x \}` is the principal order
        filter of `x` and `P(F^x; q)` is the characteristic polynomial
        of the (sub)poset `F^x`.
        """
        def __init__(self, M, prefix='C') -> None:
            """
            Initialize ``self``.

            TESTS::

                sage: L = posets.BooleanLattice(3)
                sage: M = L.quantum_moebius_algebra()
                sage: TestSuite(M.C()).run() # long time
            """
            self._basis_name = "characteristic"
            CombinatorialFreeModule.__init__(self, M.base_ring(),
                                             tuple(M._lattice),
                                             prefix=prefix,
                                             category=MoebiusAlgebraBases(M))

            # Change of basis:
            E = M.E()
            phi = self.module_morphism(self._to_natural_basis,
                                       codomain=E, category=self.category(),
                                       triangular='lower', unitriangular=True,
                                       key=M._lattice._element_to_vertex)

            phi.register_as_coercion()
            (~phi).register_as_coercion()

        @cached_method
        def _to_natural_basis(self, x):
            """
            Convert the element indexed by ``x`` to the natural basis.

            EXAMPLES::

                sage: M = posets.BooleanLattice(4).quantum_moebius_algebra()
                sage: C = M.C()
                sage: all(C(C._to_natural_basis(x)) == C.monomial(x)
                ....:     for x in C.basis().keys())
                True
            """
            M = self.realization_of()
            N = M.natural()
            q = M._q
            L = M._lattice

            def poly(x, y):
                return L.subposet(L.closed_interval(x, y)).characteristic_polynomial()
            return N.sum_of_terms((y, poly(x, y)(q=q))
                                  for y in L.order_filter([x]))

    characteristic_basis = C

    class KL(BasisAbstract):
        r"""
        The Kazhdan-Lusztig basis of a quantum Möbius algebra.

        The Kazhdan-Lusztig basis `\{ B_x \mid x \in L \}` of `M_L`
        for some lattice `L` is defined by

        .. MATH::

            B_x = \sum_{y \geq x} P_{x,y}(q) E_a,

        where `P_{x,y}(q)` is the Kazhdan-Lusztig polynomial of `L`,
        following the definition given in [EPW14]_.

        EXAMPLES:

        We construct some examples of Proposition 4.5 of [EPW14]_::

            sage: M = posets.BooleanLattice(4).quantum_moebius_algebra()
            sage: KL = M.KL()
            sage: KL[4] * KL[5]
            (q^2+q^3)*KL[5] + (q+2*q^2+q^3)*KL[7] + (q+2*q^2+q^3)*KL[13]
             + (1+3*q+3*q^2+q^3)*KL[15]
            sage: KL[4] * KL[15]
            (1+3*q+3*q^2+q^3)*KL[15]
            sage: KL[4] * KL[10]
            (q+3*q^2+3*q^3+q^4)*KL[14] + (1+4*q+6*q^2+4*q^3+q^4)*KL[15]
        """
        def __init__(self, M, prefix='KL') -> None:
            """
            Initialize ``self``.

            TESTS::

                sage: L = posets.BooleanLattice(3)
                sage: M = L.quantum_moebius_algebra()
                sage: TestSuite(M.KL()).run() # long time
            """
            self._basis_name = "Kazhdan-Lusztig"
            CombinatorialFreeModule.__init__(self, M.base_ring(),
                                             tuple(M._lattice),
                                             prefix=prefix,
                                             category=MoebiusAlgebraBases(M))

            # Change of basis:
            E = M.E()
            phi = self.module_morphism(self._to_natural_basis,
                                       codomain=E, category=self.category(),
                                       triangular='lower', unitriangular=True,
                                       key=M._lattice._element_to_vertex)

            phi.register_as_coercion()
            (~phi).register_as_coercion()

        @cached_method
        def _to_natural_basis(self, x):
            """
            Convert the element indexed by ``x`` to the natural basis.

            EXAMPLES::

                sage: M = posets.BooleanLattice(4).quantum_moebius_algebra()
                sage: KL = M.KL()
                sage: all(KL(KL._to_natural_basis(x)) == KL.monomial(x) # long time
                ....:     for x in KL.basis().keys())
                True
            """
            M = self.realization_of()
            L = M._lattice
            E = M.E()
            q = M._q
            rank = L.rank_function()
            return E.sum_of_terms((y, q**(rank(y) - rank(x)) *
                                   L.kazhdan_lusztig_polynomial(x, y)(q=q**-2))
                                  for y in L.order_filter([x]))

    kazhdan_lusztig = KL