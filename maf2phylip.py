import sys

def printAlignment(seqs):
    if len(seqs) < 4:
        return
    print(len(seqs), len(seqs[0][1]))
    for e in seqs:
        print(e[0], e[1])

alignment = []
for line in open(sys.argv[1]):
    line = line.split()
    if len(line) == 0 or (line[0] != "a" and line[0][0] != "s"):
        continue
    if line[0][0] == "a":
        printAlignment(alignment)
        alignment = []
    elif int(line[3]) > 100 and (len(line[1]) < 3 or line[1][0:3] != "Anc") :
        alignment.append((line[1], line[6]))
printAlignment(alignment)
