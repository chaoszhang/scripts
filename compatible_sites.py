import sys

K = int(sys.argv[3])

def discordance(seqs, i, j):
    M = {}
    for a in "ACGT":
        for b in "ACGT":
            M[a + b] = []
    for k in range(len(seqs)):
        seq = seqs[k]
        a = seq[i]
        b = seq[j]
        if a in "ACGT" and b in "ACGT":
            M[a + b].append(k)
    max_list = []
    for a in ["AC","AG","AT","CG","CT","GT"]:
        for b in ["AC","AG","AT","CG","CT","GT"]:
            new_list = sorted([(len(M[x + y]), M[x + y]) for x in a for y in b])[0][1]
            if len(new_list) > len(max_list):
                max_list = new_list
    return max_list

def informative(seqs):
    n = len(seqs)
    L = len(seqs[0])
    cnt = {}
    uniq = [0 for j in range(L)]
    for c in "ACGT":
        cnt[c] = [False for j in range(L)]
    for seq in seqs:
        for j in range(L):
            for c in "ACGT":
                if seq[j] == c:
                    cnt[c][j] += 1
    for c in "ACGT":
        for j in range(L):
            if cnt[c][j] >= 2:
                uniq[j] += 1
            
    for i in range(5):
        print(i, len([i for v in uniq if v == i]))

    for i in range(n):
        seqs[i] = "".join([seqs[i][j] if seqs[i][j] in "ACGT" and cnt[seqs[i][j]][j] >= 2 else "-" for j in range(L) if uniq[j] >= 2])

def filterSites(seqs, K, T, X = 5):
    n = len(seqs)
    L = len(seqs[0])
    siteL = [[0 for j in range(L)] for i in range(n)]
    siteR = [[0 for j in range(L)] for i in range(n)]
    for i in range(K):
        for sites in siteL:
            sites[i] = K - i
        for sites in siteR:
            sites[L - K + i] = i + K
    for i in range(L - K):
        for j in range(i + 1, i + 1 + K):
            sites = discordance(seqs, i, j)
            for k in sites:
                siteR[k][i] += 1
                siteL[k][j] += 1
    siteMin = [[min(siteL[i][j], siteR[i][j]) for j in range(L)] for i in range(n)]
    for i in range(n):
        seqs[i] = "".join([seqs[i][j] if sum(siteMin[i][max(0,j-X):min(L,j+X+1)]) <= T else "X" for j in range(L)])
        seqs[i] = "".join(["-" if "X" in seqs[i][max(0,j-X):min(L,j+X+1)] else seqs[i][j] for j in range(L)])
    informative(seqs)
    print("\n".join(["".join([str(siteMin[i][j]) for j in range(L)]) for i in range(n)]))
    print("\n".join(seqs))
    
def filterCols(seqs, K, T = 5):
    n = len(seqs)
    L = len(seqs[0])
    siteL = [[0 for j in range(L)] for i in range(n)]
    siteR = [[0 for j in range(L)] for i in range(n)]
    for i in range(K):
        for sites in siteL:
            sites[i] = K - i
        for sites in siteR:
            sites[L - K + i] = i + K
    for i in range(L - K):
        for j in range(i + 1, i + 1 + K):
            sites = discordance(seqs, i, j)
            for k in sites:
                siteR[k][i] += 1
                siteL[k][j] += 1
    siteCnt = [len([i for i in range(n) if min(siteL[i][j], siteR[i][j]) > 0]) for j in range(L)]
    for i in range(len(seqs)):
        seqs[i] = "".join([seqs[i][j] for j in range(L) if siteCnt[j] <= T])
    print(siteCnt)
    
seqs = []
names = []
seq = []
for line in open(sys.argv[1], "r"):
    line = line.split()[0]
    if line[0] == ">":
        names.append(line)
        if len(seq) != 0:
            seqs.append("".join(seq))
            seq = []
    else:
        seq.append(line)
seqs.append("".join(seq))

n = len(seqs)
informative(seqs)
filterCols(seqs, K, int(n / (4 * 5 + 1)))
filterSites(seqs, K, 1)
filterSites(seqs, K, 1)
filterCols(seqs, K, 5)
filterSites(seqs, K, 0, X = 0)
filterSites(seqs, K, 0, X = 0)

'''
for T in range(K, minT, -1):
    filterSites(seqs, K, 1)
    L = len(seqs[0])
    conflictL = [0 for i in range(L)]
    conflictR = [0 for i in range(L)]
    for i in range(K):
        conflictL[i] = K - i
        conflictR[L - K + i] = i + K
    for i in range(L - K):
        for j in range(i + 1, i + 1 + K):
            if len(discordance(seqs, i, j)) > 0:
                conflictR[i] += 1
                conflictL[j] += 1
    
    conflict = [min(conflictL[i], conflictR[i]) for i in range(L)]
    print(conflict)
    print(T)
    
    for i in range(len(seqs)):
        seqs[i] = "".join([seqs[i][j] for j in range(L) if conflict[j] < T])
    
    filterSites(seqs, K, 0)
'''

with open(sys.argv[2], "w") as f:
    for i in range(len(seqs)):
        f.write(names[i])
        f.write("\n")
        f.write(seqs[i])
        f.write("\n")
        