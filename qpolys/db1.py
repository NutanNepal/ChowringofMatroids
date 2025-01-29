from sage.all import *

def cmp_elements_key(x):
    """
    A helper function to compare elements which may be integers or strings.

    EXAMPLES::

        sage: from sage.matroids.utilities import cmp_elements_key
        sage: l = ['a', 'b', 1, 3, 2, 10, 111, 100, 'c', 'aa']
        sage: sorted(l, key=cmp_elements_key)
        [1, 2, 3, 10, 100, 111, 'a', 'aa', 'b', 'c']
    """
    return (isinstance(x, str), x)

def characteristic_polynomial(M, la=None):
    R = ZZ['l']
    w = whitney_numbers(M)
    w.reverse()
    chi = R(w)
    if la is not None:
        return chi(la)
    return chi

def whitney_numbers(M):
    abs_w = [0] * (M.rank() + 1)
    for S in no_broken_circuits_sets_iterator(M):
        abs_w[len(S)] += 1
    return [ZZ((-1)**i * val) for i, val in enumerate(abs_w) if val != 0]

def no_broken_circuits_sets_iterator(M, ordering=None):
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
                