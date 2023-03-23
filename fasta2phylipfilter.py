import sys

seqs = {}
for line in open(sys.argv[1], "r"):
    line = line.split()[0]
    if line[0] == ">":
        name = line[1:]
        seqs[name] = []
    else:
        seqs[name].append(line)

realseqs = {}
for name in seqs:
    seq = "".join(seqs[name])
    if len([c for c in seq if c != '-']) != 0:
        realseqs[name] = seq
        somename = name

print(str(len(realseqs)) + "\t" + str(len(realseqs[somename])))
for name in realseqs:
    print(name + "\t" + realseqs[name])