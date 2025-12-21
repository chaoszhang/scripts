import sys
import re
import random

sys.setrecursionlimit(100000)

def parseNewickHelper(nw, i, p):
    cur = {"P": p, "isroot": p is None, "children": []}
    if nw[i] == "(":
        child, i = parseNewickHelper(nw, i + 1, cur)
        cur["children"].append(child)
        while nw[i] != ")":
            while nw[i] != "," and nw[i] != ")":
                i += 1
            if nw[i] == ",":
                child, i = parseNewickHelper(nw, i + 1, cur)
                cur["children"].append(child)
        cur["isleaf"] = False
    else:
        cur["label"] = nw[i]
        cur["isleaf"] = True
    i += 1
    while nw[i] not in ",);":
        i += 1
    return cur, i

def parseNewick(nw):
    return parseNewickHelper([e for e in re.split("([(,:);])", nw) if e != ""], 0, None)[0]

def printNewick(t):
    if t["isleaf"]:
        return t["label"]
    else:
        return "(" + ",".join([printNewick(child) for child in t["children"]]) + ")"

MAXRAND = 2 ** 512
def randomLeafHash():
    return (random.randrange(MAXRAND) ^ random.randrange(MAXRAND)) + random.randrange(MAXRAND)

def assignLeafHash(cur, RLeafHash):
    if cur["isleaf"]:
        RLeafHash[cur["label"]] = randomLeafHash()
    else:
        for child in cur["children"]:
            assignLeafHash(child, RLeafHash)

def mapLeafHash(cur, RLeafHash, QLeafHash):
    if cur["isleaf"]:
        label = cur["label"]
        if label in RLeafHash:
            QLeafHash[label] = RLeafHash[label]
    else:
        for child in cur["children"]:
            mapLeafHash(child, RLeafHash, QLeafHash)

def tree2set(cur, TSet, QLeafHash, QRootHash, QTrivialHash):
    if cur["isleaf"]:
        label = cur["label"]
        if label in QLeafHash:
            return QLeafHash[label]
        else:
            return 0
    else:
        nodeHash = sum([tree2set(child, TSet, QLeafHash, QRootHash, QTrivialHash) for child in cur["children"]])
        minHash = min(nodeHash, QRootHash - nodeHash)
        if minHash not in QTrivialHash:
            TSet.add(minHash)
        return nodeHash

if len(sys.argv) != 3:
    print("python3 compareTree.py ref.nw queries.nw", file=sys.stderr)
    print("ref.nw: one Newick tree in one line", file=sys.stderr)
    print("queries.nw: N Newick trees in N lines", file=sys.stderr)
    print("stdout: FN, FP, TP, and NRF in queries.nw order", file=sys.stderr)
    quit()
    

R = parseNewick(open(sys.argv[1]).readline())
RLeafHash = {}
assignLeafHash(R, RLeafHash)

print("FN: only in reference tree", file=sys.stderr)
print("FP: only in query tree", file=sys.stderr)
print("TP: in both trees", file=sys.stderr)
print("NRF: normalized RF distance", file=sys.stderr)

print("FN", "FP", "TP", "NRF")
for line in open(sys.argv[2]):
    Q = parseNewick(line)
    QLeafHash = {}
    mapLeafHash(Q, RLeafHash, QLeafHash)
    QRootHash = sum([QLeafHash[e] for e in QLeafHash])
    QTrivialHash = frozenset([0] + [min(QLeafHash[e], QRootHash - QLeafHash[e]) for e in QLeafHash])
    RSet = set()
    tree2set(R, RSet, QLeafHash, QRootHash, QTrivialHash)
    RSet = frozenset(RSet)
    QSet = set()
    tree2set(Q, QSet, QLeafHash, QRootHash, QTrivialHash)
    QSet = frozenset(QSet)
    TP = len(RSet & QSet)
    FN = len(RSet) - TP
    FP = len(QSet) - TP
    NRF = (FN + FP) / (FN + FP + 2 * TP) if FN + FP + 2 * TP > 0 else "NA"
    print(FN, FP, TP, NRF)