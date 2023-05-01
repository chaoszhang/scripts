import sys

first = True
for line in open(sys.argv[1], "r"):
    line = line.split()[0]
    if line[0] != ">":
        if first:
            first = False
            L = len(line)
            cntA = [0 for i in range(L)]
            cntC = [0 for i in range(L)]
            cntG = [0 for i in range(L)]
            cntT = [0 for i in range(L)]
            cnt2 = [[] for i in range(L)]
            include = [False for i in range(L)]
        for i in range(L):
            if line[i] == 'A':
                cntA[i] += 1
            if line[i] == 'C':
                cntC[i] += 1
            if line[i] == 'G':
                cntG[i] += 1
            if line[i] == 'T':
                cntT[i] += 1
for i in range(L):
    if cntA[i] > 1:
        cnt2[i].append("A")
    if cntC[i] > 1:
        cnt2[i].append("C")
    if cntG[i] > 1:
        cnt2[i].append("G")
    if cntT[i] > 1:
        cnt2[i].append("T")
    if (len(cnt2[i]) == 2 or len(cnt2[i]) == 3) and cntA[i] + cntC[i] + cntG[i] + cntT[i] >= 50:
        include[i] = True
if len([b for b in include if b]) >= 50:
    with open(sys.argv[2], "w") as f:
        for line in open(sys.argv[1], "r"):
            line = line.split()[0]
            if line[0] == ">":
                f.write(line + "\n")
            else:
                f.write("".join([line[i] if line[i] in cnt2[i] else '-' for i in range(L) if include[i]]) + "\n")