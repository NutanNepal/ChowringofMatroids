from sage.all import *
from typing import Iterator, List, Optional, Union

R = PolynomialRing(QQ, 't')
t = R.gen()
    
def cmp_elements_key(x: Union[int, str]) -> tuple:
    """
    A helper function to compare elements which may be integers or strings.

    EXAMPLES::
        sage: from sage.matroids.utilities import cmp_elements_key
        sage: l = ['a', 'b', 1, 3, 2, 10, 111, 100, 'c', 'aa']
        sage: sorted(l, key=cmp_elements_key)
        [1, 2, 3, 10, 100, 111, 'a', 'aa', 'b', 'c']
    """
    return (isinstance(x, str), x)

def characteristic_polynomial(M: Matroid, la: Optional[int] = None) -> Polynomial:
    """
    Compute the characteristic polynomial of a matroid.

    :param M: A matroid.
    :param la: Optional; if provided, evaluate the polynomial at this value.
    :return: The characteristic polynomial of the matroid.
    """
    R = ZZ['t']
    w = whitney_numbers(M)
    w.reverse()
    chi = R(w)
    if la is not None:
        return chi(la)
    return chi

def whitney_numbers(M: Matroid) -> List[int]:
    """
    Compute the Whitney numbers of the second kind for a matroid.

    :param M: A matroid.
    :return: A list of Whitney numbers.
    """
    abs_w = [0] * (M.rank() + 1)
    for S in no_broken_circuits_sets_iterator(M):
        abs_w[len(S)] += 1
    return [ZZ((-1)**i * val) for i, val in enumerate(abs_w) if val != 0]

def no_broken_circuits_sets_iterator(M: Matroid, ordering: Optional[List] = None) -> Iterator[frozenset]:
    """
    Iterate over all no broken circuit sets of a matroid.

    :param M: A matroid.
    :param ordering: Optional; a specific ordering of the groundset.
    :return: An iterator over no broken circuit sets.
    """
    if M.loops():
        return
    if ordering is None:
        rev_order = sorted(M.groundset(), key=cmp_elements_key, reverse=True)
    else:
        if frozenset(ordering) != M.groundset():
            raise ValueError("not an ordering of the groundset")
        rev_order = list(reversed(ordering))
    
    Tmax = len(rev_order)
    reverse_dict = {value: key for key, value in enumerate(rev_order)}
    yield frozenset()
    next_level = [[val] for val in rev_order]
    level = -1
    
    while next_level:
        cur_level = next_level
        next_level = []
        level += 1
        for H in cur_level:
            tp = reverse_dict[H[level]] + 1
            is_indep = True
            Ht = [None] * (Tmax - tp)
            for i in range(tp, Tmax):
                temp = H + [rev_order[i]]
                if not M._is_independent(frozenset(temp)):
                    is_indep = False
                    break
                Ht[i - tp] = temp
            if is_indep:
                yield frozenset(H)
                next_level.extend(Ht)

def is_graphic(matroid: Matroid) -> bool:
    """
    Check if a matroid is graphic.

    :param matroid: A matroid.
    :return: True if the matroid is graphic, False otherwise.
    """
    from sage.matroids.database_matroids import (
        U24,
        Fano,
        FanoDual,
        K5dual,
        K33dual
    )
    excluded_minors = [U24(), Fano(), FanoDual(), K5dual(), K33dual()]
    for M in excluded_minors:
        if matroid.has_minor(M):
            return False
    return True

#########################

def is_paving(M):
    n = M.size()
    r = M.rank()
    return (len(M.independent_r_sets(r-1)) == binomial(n, r-1))

def kazhdan_lusztig_inverse_uniform(k: int, n: int) -> Polynomial:
    """
    Compute the inverse Kazhdan-Lusztig polynomial for a uniform matroid.

    :param k: Rank of the matroid.
    :param n: Size of the groundset.
    :return: The inverse Kazhdan-Lusztig polynomial.
    """
    if k == n:
        return R(1)
    d = k
    m = n - d
    ans = 0
    for j in range((d - 1) // 2 + 1):
        ans += m * (d - 2 * j) / ((m + j) * (m + d - j)) * binomial(d, j) * t**j
    return ans * binomial(m + d, d)

def invkl(M: Matroid) -> Polynomial:
    """
    Compute the inverse Kazhdan-Lusztig polynomial for a matroid.

    :param M: A matroid.
    :return: The inverse Kazhdan-Lusztig polynomial.
    """
    if M.loops():
        return R(0)
    k, n = M.rank(), M.size()
    if k == n or k == 0:
        return R(1)
    if not M.is_connected():
        ans = R(1)
        CC = M.components()
        for N in CC:
            res = M.delete(M.groundset() - N)
            ans = ans * invkl(res)
        return ans

    if is_paving(M):
        return kl_inverse_paving(M)
    if is_paving(M.dual()):
        return kl_inverse_copaving(M)

    LF = M.lattice_of_flats()
    ans = R(0)
    for F in LF:
        if len(F) != n:
            Res = M.delete(M.groundset() - F)
            Con = M.contract(F)
            chi = characteristic_polynomial(Con)(1 / t) * t ** (Con.rank())
            PPP = invkl(Res)(t) * (-1) ** (Res.rank())
            ans += chi * PPP
    assert (t**k * ans(1 / t)).numerator() == -ans(t)
    ans = ans.numerator() * (-1) ** (k + 1)
    return ans.truncate((k + 1) // 2)

def kl_inverse_paving(M: Matroid) -> Polynomial:
    """
    Compute the inverse Kazhdan-Lusztig polynomial for a paving matroid.

    :param M: A paving matroid.
    :return: The inverse Kazhdan-Lusztig polynomial.
    """
    assert is_paving(M)
    n = M.size()
    k = M.rank()
    ans = kazhdan_lusztig_inverse_uniform(k, n)
    for H in M.hyperplanes():
        h = len(H)
        if h >= k:
            ans -= q_kl(k, h)
    return ans

def kl_inverse_copaving(M: Matroid) -> Polynomial:
    """
    Compute the inverse Kazhdan-Lusztig polynomial for a copaving matroid.

    :param M: A copaving matroid.
    :return: The inverse Kazhdan-Lusztig polynomial.
    """
    assert is_paving(M.dual())
    n = M.size()
    k = M.rank()
    ans = kazhdan_lusztig_inverse_uniform(k, n)
    for H in M.dual().hyperplanes():
        h = len(H)
        if h >= n - k:
            ans -= kli_vtilde_dual(n - k, h, n) + kazhdan_lusztig_inverse_uniform(h - n + k + 1, h) * kazhdan_lusztig_inverse_uniform(n - h - 1, n - h)
    return ans

def q_kl(k: int, h: int) -> Polynomial:
    """
    Compute the q_kl polynomial.

    :param k: Rank parameter.
    :param h: Size parameter.
    :return: The q_kl polynomial.
    """
    return kazhdan_lusztig_inverse_uniform(k, h + 1) - kazhdan_lusztig_inverse_uniform(k - 1, h)

def kli_vtilde_dual(k: int, h: int, n: int) -> Polynomial:
    """
    Compute the kli_vtilde_dual polynomial.

    :param k: Rank parameter.
    :param h: Size parameter.
    :param n: Groundset size.
    :return: The kli_vtilde_dual polynomial.
    """
    return helper1(n - k, h, n)

def helper1(k: int, h: int, n: int) -> Polynomial:
    """
    Helper function for kli_vtilde_dual.

    :param k: Rank parameter.
    :param h: Size parameter.
    :param n: Groundset size.
    :return: A polynomial.
    """
    c = n - h
    ans1 = kazhdan_lusztig_inverse_uniform(k, n)
    ans2 = helper2(c, k, n)
    ans3 = kazhdan_lusztig_inverse_uniform(k - c + 1, h) * kazhdan_lusztig_inverse_uniform(c - 1, c)
    return ans1 - ans2 + ans3

def helper2(c: int, k: int, n: int) -> Polynomial:
    """
    Helper function for helper1.

    :param c: Parameter.
    :param k: Rank parameter.
    :param n: Groundset size.
    :return: A polynomial.
    """
    h = n - c
    ans = 0
    for j in range(k - c + 1):
        ans += binomial(n - c, j) * (-1) ** (c - 1 + j) * kazhdan_lusztig_inverse_uniform(c - 1, c) * t ** (k - c - j + 1) * chuly(k - c - j + 1, n - c - j)(1 / t)
    for i in range(c - 1):
        for j in range(k - i):
            ans += binomial(c, i) * binomial(n - c, j) * (-1) ** (i + j) * t ** (k - i - j) * helper4(c, k, n, i, j)(1 / t)
    ans = ans.numerator().truncate((k - 1) // 2 + 1)
    if ans[0] < 0:
        ans = -ans
    return ans

def helper4(c: int, k: int, n: int, i: int, j: int) -> Polynomial:
    """
    Helper function for helper2.

    :param c: Parameter.
    :param k: Rank parameter.
    :param n: Groundset size.
    :param i: Index.
    :param j: Index.
    :return: A polynomial.
    """
    ans = 0
    for l in range(c - i - 1):
        ans += (-1) ** l * (t - 1) ** (max(n - i - j - l - 1, 0))
    for u in range(n - k - 1):
        ans = doit_once(ans)
    return ans

def chuly(a: int, b: int) -> Polynomial:
    """
    Compute the chuly polynomial.

    :param a: Parameter.
    :param b: Parameter.
    :return: The chuly polynomial.
    """
    ans = (t - 1) ** b
    for i in range(b - a):
        ans = doit_once(ans)
    return ans

def doit_once(p: Polynomial) -> Polynomial:
    """
    Perform a single step of the chuly computation.

    :param p: A polynomial.
    :return: The transformed polynomial.
    """
    p = p // t**2
    p = p * t
    p = p - p(1)
    return p

#########################

def kl(M):
    return M.lattice_of_flats().kazhdan_lusztig_polynomial()(t)

def qhat(M):
    S = PolynomialRing(ZZ, 't')
    return S((-1) ** M.rank() * invkl(M)(t))

def lattice_kl(L):
    return L.kazhdan_lusztig_polynomial()(t)

def parallel_connection(m, n):
    G = graphs.CycleGraph(m + n - 2)
    G.add_edge(0, m-1)
    edge_e = frozenset({(0, m - 1)})
    return G, edge_e

def uniformQpoly(r: int, n: int) -> Polynomial:
    """
    Compute the uniform Q-polynomial for given parameters.

    :param r: Rank of the matroid.
    :param n: Size of the groundset.
    :return: The uniform Q-polynomial.
    """
    m, d = n - r, r
    R = PolynomialRing(QQ, 't')
    t = R.gen()
    upper_bound = (d - 1) // 2
    sum = R(0)
    for j in range(0, upper_bound + 1):
        coeff = m * (d - 2 * j) / ((m + j) * (m + d - j)) * binomial(d, j)
        sum += coeff * t**j
    return binomial(m + d, d) * sum

def uniformKLpoly(r: int, n: int) -> Polynomial:
    """
    Compute the uniform KL-polynomial for given parameters.

    :param r: Rank of the matroid.
    :param n: Size of the groundset.
    :return: The uniform KL-polynomial.
    """
    m, d = n - r, r
    R = PolynomialRing(QQ, 't')
    t = R.gen()
    upper_bound = (d - 1) // 2
    sum = R(0)
    for i in range(0, upper_bound + 1):
        s = R(0)
        for h in range(0, m):
            s += binomial(d - i + h, h + i + 1) * binomial(i - 1 + h, h)
        s *= binomial(m + d, i) / (d - i)
        sum += s * t**i
    return sum