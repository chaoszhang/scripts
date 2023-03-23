import sys

with open(sys.argv[2], "w") as f:
    n = int(sys.argv[3])
    L = int(sys.argv[4])
    ntaxon = 0
    f.write("#NEXUS\nbegin DATA;\n\tdimensions ntax=" + sys.argv[3] + " nchar=" + sys.argv[4] + ";\n\tformat missing=N gap=- datatype=dna;\n\toptions gapmode=missing;\n\tMATRIX\n")
    for line in open(sys.argv[1], "r"):
        line = line.split()[0]
        if line[0] == ">":
            seqlen = 0
            ntaxon += 1
            if ntaxon > n:
                break
            f.write(line[1:] + "\t")
        else:
            if seqlen < L:
                if seqlen + len(line) >= L:
                    f.write(line[0:L-seqlen] + "\n")
                    seqlen = L
                else:
                    f.write(line)
                    seqlen += len(line)
    f.write("\t;\nend;\n")