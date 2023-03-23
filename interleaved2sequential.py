import sys

headline = True
for line in open(sys.argv[1], "r"):
    line = line.split("\n")[0]
    if headline:
        headline = False
        cnt = 0
        total = 1 + int(line.split()[0])
        seqs = [[] for i in range(total)]
    seqs[cnt % total].append(line)
    cnt += 1
for seq in seqs:
    print("".join(seq))