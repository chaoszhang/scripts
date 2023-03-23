import sys

with open(sys.argv[2], "a") as f:
    n = int(sys.argv[3])
    L = int(sys.argv[4])
    ntaxon = 0
    f.write(sys.argv[3] + "\t" + sys.argv[4] + "\n")
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