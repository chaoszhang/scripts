import sys

removed = {}
for name in [sys.argv[i] for i in range(2, len(sys.argv))]:
    removed[name] = name

headline = True
for line in open(sys.argv[1], "r"):
    line = line.split()
    if headline:
        headline = False
        n = int(line[0])
        L = line[1]
        cnt = n
        seq = []
    else:
        if line[0] in removed:
            n -= 1
        else:
            seq.append(line[0] + "\t" + line[1])
        cnt -= 1
        if cnt == 0:
            headline = True
            print(str(n) + "\t" + L)
            for s in seq:
                print(s)