import sys
import math
from scipy import stats
from scipy.stats import binom, norm
import numpy as np

def z2lgp(z, two_sided=True):
    # For large z, use log10(pdf(z)) - log10(z)
    if np.abs(z) > 7:  
        # Compute log10(pdf(x)) manually
        log_p = np.log10(1 / np.sqrt(2 * np.pi)) - (z ** 2 / 2) * np.log10(np.exp(1)) - np.log10(np.abs(z))
        if two_sided:
            # Multiply by 2 for two-sided p-value
            log_p += np.log10(2)
    else:
        if two_sided:
            # Multiply by 2 for two-sided p-value
            p = 2 * stats.norm.sf(np.abs(z))
        else:
            p = stats.norm.sf(z)
        # Use np.log10 to compute logarithm, adding a small value to avoid log10(0)
        log_p = np.log10(p + np.finfo(float).eps)
    return log_p
    
chrs = [str(i) for i in range(1, 23)] + ["X"]
total = {}
nb = 1 + 237
seg = {}
cnt = 0
midA = [0 for i in range(nb)]
midB = [0 for i in range(nb)]
midC = [0 for i in range(nb)]
midD = [0 for i in range(nb)]
midT = [0 for i in range(nb)]
madA = [0 for i in range(nb)]
madB = [0 for i in range(nb)]
madC = [0 for i in range(nb)]
madD = [0 for i in range(nb)]
madT = [0 for i in range(nb)]
zscoreA = [[] for i in range(nb)]
zscoreB = [[] for i in range(nb)]
zscoreC = [[] for i in range(nb)]
zscoreD = [[] for i in range(nb)]
zscoreT = [[] for i in range(nb)]
topD = [0 for i in range(nb)]
topT = [0 for i in range(nb)]
btmD = [0 for i in range(nb)]
btmT = [0 for i in range(nb)]

bnorm = [[] for i in range(nb)]
A = [[] for i in range(nb)]
B = [[] for i in range(nb)]
C = [[] for i in range(nb)]
D = [[] for i in range(nb)]
T = [[] for i in range(nb)]
for branch in range(1, nb):
    bv = {}
    for chromosome in chrs:
        S0 = []
        S1 = []
        S2 = []
        S3 = []
        pos = []
        segid = 0
        lastSum = 0
        headline = True
        for line in open("sliding/" + str(branch) + "/chr" + chromosome + ".tsv"):
            line = line.split()
            if headline:
                headline = False
                continue
            if not (chromosome, line[0]) in total:
                total[(chromosome, line[0])] = []
            pos.append(line[0])
            s1 = float(line[1])
            s2 = float(line[2])
            s3 = float(line[3])
            s0 = s1 + s2 + s3
            if s0 != 0:
                cnt += 1
            S0.append(s0)
            S1.append(s1)
            S2.append(s2)
            S3.append(s3)
            bv[(chromosome, line[0])] = s0
            if branch == nb - 1:
                if lastSum == 0 and s0 != 0 and (chromosome, line[0]) != ("1", "125000000") and (chromosome, line[0]) != ("5", "47000000") and (chromosome, line[0]) != ("14", "16000000"):
                    segid += 1
                seg[(chromosome, line[0])] = str(max(segid, 1)) if chromosome not in ["21", "22"] else "1"
                lastSum = s0
        for i in range(len(S0)):
            if i != 0 and i != len(S0) - 1 and S0[i - 1] != 0 and S0[i] != 0 and S0[i + 1] != 0:
                A[branch].append(S1[i])
                B[branch].append(S2[i])
                C[branch].append(S3[i])
    L = len(C[branch])
    D[branch] = [A[branch][i] - B[branch][i] for i in range(L)]
    T[branch] = [A[branch][i] + B[branch][i] + C[branch][i] for i in range(L)]
    topD[branch] = sorted(D[branch])[int(L * 0.975)]
    topT[branch] = sorted(T[branch])[int(L * 0.975)]
    btmD[branch] = sorted(D[branch])[int(L * 0.025)]
    btmT[branch] = sorted(T[branch])[int(L * 0.025)]
    midA[branch] = sorted(A[branch])[int(L / 2)]
    midB[branch] = sorted(B[branch])[int(L / 2)]
    midC[branch] = sorted(C[branch])[int(L / 2)]
    midD[branch] = sorted(D[branch])[int(L / 2)]
    midT[branch] = sorted(T[branch])[int(L / 2)]
    madA[branch] = sorted([abs(x - midA[branch]) for x in A[branch]])[int(L / 2)]
    madB[branch] = sorted([abs(x - midB[branch]) for x in B[branch]])[int(L / 2)]
    madC[branch] = sorted([abs(x - midC[branch]) for x in C[branch]])[int(L / 2)]
    madD[branch] = sorted([abs(x - midD[branch]) for x in D[branch]])[int(L / 2)]
    madT[branch] = sorted([abs(x - midT[branch]) for x in T[branch]])[int(L / 2)]
    zscoreA[branch] = [0.6745 * (x - midA[branch]) / madA[branch] for x in A[branch]]
    zscoreB[branch] = [0.6745 * (x - midB[branch]) / madB[branch] for x in B[branch]]
    zscoreC[branch] = [0.6745 * (x - midC[branch]) / madC[branch] for x in C[branch]]
    zscoreD[branch] = [0.6745 * (x - midD[branch]) / madD[branch] for x in D[branch]]
    zscoreT[branch] = [0.6745 * (x - midT[branch]) / madT[branch] for x in T[branch]]
    
    
    bnorm[branch] = midA[branch] + midB[branch] + midC[branch]
    '''
    D[branch] = [(A[branch][i] - B[branch][i] - normA[branch] + normB[branch]) / (normA[branch] + normB[branch]) for i in range(L)]
    T[branch] = [(A[branch][i] + B[branch][i] + C[branch][i]) / bnorm[branch] for i in range(L)]
    A[branch] = [v / normA[branch] for v in A[branch]]
    B[branch] = [v / normB[branch] for v in B[branch]]
    C[branch] = [v / normC[branch] for v in C[branch]]
    '''
    for e in bv:
        total[e].append(bv[e] / bnorm[branch])
for e in total:
    total[e] = sorted(total[e])[int(len(total[e])/2)]
#for e in total:
#    if total[e] < 0.1:
#        total[e] = 0

zcutoff = 5.382228
print("cnt:", cnt)
with open("stat_test.tsv", "w") as f:
    f.write("\t".join(["Category", "Value"]) + "\n")
    for branch in range(1, nb):
        for j in range(len(zscoreA[branch])):
            f.write("\t".join(["D", str(zscoreD[branch][j])]) + "\n")
            f.write("\t".join(["T", str(zscoreT[branch][j])]) + "\n")
#exit(0)

outstanding = [{} for i in range(nb)]
pattern = [[0 for j in range(6)] for i in range(nb)]
outstandingCnt = []
outstandingCnt2 = []

with open("sliding_norm.tsv", "w") as f1, open("sliding.tsv", "w") as f2, open("stat_test_outlier.tsv", "w") as f3, open("stat_test_all.tsv", "w") as f4:
    f1.write("\t".join(["Branch", "Chr", "Pos", "Topology", "Score", "Seg"]) + "\n")
    f2.write("\t".join(["Branch", "Chr", "Pos", "Topology", "Score", "Seg"]) + "\n")
    f3.write("\t".join(["Branch", "Chr", "Pos", "Category", "Value"]) + "\n")
    f4.write("\t".join(["Branch", "Chr", "Pos", "Category", "Value"]) + "\n")
    for branch in range(1, nb):
        for chromosome in chrs:
            headline = True
            chrD = []
            chrT = []
            for line in open("sliding/" + str(branch) + "/chr" + chromosome + ".tsv"):
                line = line.split()
                if headline:
                    headline = False
                    outgroup = line
                    continue
                s = total[(chromosome, line[0])] * bnorm[branch]
                s1 = float(line[1])
                s2 = float(line[2])
                s3 = float(line[3])
                chrD.append(s1 - s2)
                chrT.append(s1 + s2 + s3)
                if s == 0:
                    f1.write("\t".join([str(branch), chromosome, line[0], outgroup[1], "NaN", seg[(chromosome, line[0])]]) + "\n")
                    f1.write("\t".join([str(branch), chromosome, line[0], outgroup[2], "NaN", seg[(chromosome, line[0])]]) + "\n")
                    f1.write("\t".join([str(branch), chromosome, line[0], outgroup[3], "NaN", seg[(chromosome, line[0])]]) + "\n")
                    f2.write("\t".join([str(branch), chromosome, line[0], outgroup[1], "NaN", seg[(chromosome, line[0])]]) + "\n")
                    f2.write("\t".join([str(branch), chromosome, line[0], outgroup[2], "NaN", seg[(chromosome, line[0])]]) + "\n")
                    f2.write("\t".join([str(branch), chromosome, line[0], outgroup[3], "NaN", seg[(chromosome, line[0])]]) + "\n")
                else:
                    if abs(0.6745 * (s1 - s2 - midD[branch]) / madD[branch]) > zcutoff:
                        outstanding[branch][(chromosome, "ILS")] = 1
                        outstandingCnt.append((branch, chromosome))
                        f3.write("\t".join([str(branch), chromosome, line[0], "D", str(z2lgp(0.6745 * (s1 - s2 - midD[branch]) / madD[branch]))]) + "\n")
                    if abs(0.6745 * (s1 + s2 + s3 - midT[branch]) / madT[branch]) > zcutoff:
                        outstanding[branch][(chromosome, "signal")] = 1
                        outstandingCnt2.append((branch, chromosome))
                        f3.write("\t".join([str(branch), chromosome, line[0], "T", str(z2lgp(0.6745 * (s1 + s2 + s3 - midT[branch]) / madT[branch]))]) + "\n")
                    f4.write("\t".join([str(branch), chromosome, line[0], "D", str(z2lgp(0.6745 * (s1 - s2 - midD[branch]) / madD[branch]))]) + "\n")
                    f4.write("\t".join([str(branch), chromosome, line[0], "T", str(z2lgp(0.6745 * (s1 + s2 + s3 - midT[branch]) / madT[branch]))]) + "\n")
                    s = bnorm[branch]
                    f1.write("\t".join([str(branch), chromosome, line[0], outgroup[1], str((s1-(s1+s2)/2) / s), seg[(chromosome, line[0])]]) + "\n")
                    f1.write("\t".join([str(branch), chromosome, line[0], outgroup[2], str((s2-(s1+s2)/2) / s), seg[(chromosome, line[0])]]) + "\n")
                    f1.write("\t".join([str(branch), chromosome, line[0], outgroup[3], str((s3-(s1+s2)/2) / s), seg[(chromosome, line[0])]]) + "\n")
                    
                    f2.write("\t".join([str(branch), chromosome, line[0], outgroup[1], str(float(line[1]) / s), seg[(chromosome, line[0])]]) + "\n")
                    f2.write("\t".join([str(branch), chromosome, line[0], outgroup[2], str(float(line[2]) / s), seg[(chromosome, line[0])]]) + "\n")
                    f2.write("\t".join([str(branch), chromosome, line[0], outgroup[3], str(float(line[3]) / s), seg[(chromosome, line[0])]]) + "\n")
            cntChrD = 0
            cntChrT = 0
            cntChr = 0
            for i in range(len(chrT)):
                if i != 0 and i != len(chrT) - 1 and chrT[i - 1] != 0 and chrT[i] != 0 and chrT[i + 1] != 0:
                    cntChr += 1
                    if abs(chrD[i] - midD[branch]) > madD[branch]:
                        cntChrD += 1
                    if abs(chrT[i] - midT[branch]) > madT[branch]:
                        cntChrT += 1
            if 1 - binom.cdf(cntChrD, cntChr, 0.5) < 0.05 / 237 / 23:
                print("ILS", branch, chromosome, 1 - binom.cdf(cntChrD, cntChr, 0.5))
            if 1 - binom.cdf(cntChrT, cntChr, 0.5) < 0.05 / 237 / 23:
                print("Signal", branch, chromosome, 1 - binom.cdf(cntChrT, cntChr, 0.5))

print("Auto:", [i for i in range(nb) if len([e for e in outstanding[i] if e[0] != "X"]) > 0])
print("X:", [i for i in range(nb) if len([e for e in outstanding[i] if e[0] == "X"]) > 0])
print("Auto:", [(i, set([e[1] for e in outstanding[i] if e[0] != "X"])) for i in range(nb) if len([e for e in outstanding[i] if e[0] != "X"]) > 0])
print("X:", [(i, set([e[1] for e in outstanding[i] if e[0] == "X"])) for i in range(nb) if len([e for e in outstanding[i] if e[0] == "X"]) > 0])
print("Auto:", [(i, set([e for e in outstanding[i] if e[0] != "X"])) for i in range(nb) if len([e for e in outstanding[i] if e[0] != "X"]) > 0])
print("X:", [(i, set([e for e in outstanding[i] if e[0] == "X"])) for i in range(nb) if len([e for e in outstanding[i] if e[0] == "X"]) > 0])

print()
print("All:", [i for i in range(nb) if len(outstanding[i]) > 0])
print("All:", [(i, set([e[1] for e in outstanding[i]])) for i in range(nb) if len(outstanding[i]) > 0])
print("All:", [(i, set(outstanding[i])) for i in range(nb) if len(outstanding[i]) > 0])

print(len(outstandingCnt))
print(len(outstandingCnt2))