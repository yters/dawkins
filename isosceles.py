import os
import sys
from itertools import combinations

# Dictionary of unique subsequences, built from previous unique subsequences.
def lzd(sequence):
    d = set()
    w = ''
    for c in sequence:
        w += c
        if not w in d:
            d.add(w)
            w = ''
    return d

# Probability of randomly selected item appearing in both sets.
def jd(a, b): return 1-len(a & b)/float(len(a | b))

if __name__ == "__main__":
    print('Loading sequences.')
    path = sys.argv[1]
    sequences = {name: open(os.path.join(path, name)).read() for name in os.listdir(path)}

    print('Creating dictionaries.')
    dicts = {name: lzd(g) for name, g in sequences.items()}
    dists = {tuple(sorted([na, nb])): jd(a, b) for (na, a), (nb, b) in combinations(dicts.items(), 2)}

    print('Finding acute violations.')
    violations = 0
    results = open('results.txt', 'w')
    for na, nb, nc in combinations(dicts.keys(), 3):
        ab = dists[tuple(sorted([na, nb]))]
        ac = dists[tuple(sorted([na, nc]))]
        bc = dists[tuple(sorted([nb, nc]))]
        s1, s2, s3 = sorted([ab, bc, ac])
        if s2-s1 < s3-s2: 
            violations += 1
            results.write(na + ' ' + nb + ' ' + nc + '\n')

    count = len(sequences)
    unique_triplets = count * (count-1) * (count-2) // 6
    print('Unique triplets:', unique_triplets)
    print('Violations:', violations)
