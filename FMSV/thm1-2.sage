def rec_klp(M):
    rank = M.rank()

    if rank == 0:
        return 1
    
    for i in range(rank + 1):
        flats = sorted([sorted(F) for F in M.flats(2)])
