import sys

with open(sys.argv[2], "w") as f:
    n = int(sys.argv[3])
    L = int(sys.argv[4])
    p = int(sys.argv[5])
    nameMap = {}
    ntaxon = 0
    nCopy = p
    f.write("#NEXUS\nbegin DATA;\n\tdimensions ntax=" + str(n * p) + " nchar=" + sys.argv[4] + ";\n\tformat missing=N gap=- datatype=dna;\n\toptions gapmode=missing;\n\tMATRIX\n")
    for line in open(sys.argv[1], "r"):
        line = line.split()[0]
        if line[0] == ">":
            seqlen = 0
            nCopy += 1
            if nCopy > p:
                ntaxon += 1
                nCopy = 1
                nameMap[line[1:]] = []
            if ntaxon > n:
                break
            nameMap[line[1:]].append(line[1:] + "_" + str(nCopy))
            f.write(line[1:] + "_" + str(nCopy) + "\t")
        else:
            if seqlen < L:
                if seqlen + len(line) >= L:
                    f.write(line[0:L-seqlen] + "\n")
                    seqlen = L
                else:
                    f.write(line)
                    seqlen += len(line)
    f.write("\t;\nend;\n")
    f.write("\nbegin SETS;\n\ttaxpartition species=\n")
    for name in nameMap:
        f.write(name + ":\t" + " ".join(nameMap[name]) + ",\n")
    f.write("\t;\nend;\n")