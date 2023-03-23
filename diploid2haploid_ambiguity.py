import sys

block = []
first = False
n = 0

ambiguity = {
    "AA":"A", "AC":"M", "AG":"R", "AT":"W",
    "CA":"M", "CC":"C", "CG":"S", "CT":"Y",
    "GA":"R", "GC":"S", "GG":"G", "GT":"K",
    "TA":"W", "TC":"Y", "TG":"K", "TT":"T"
}

with open(sys.argv[2], "w") as f1:
    with open(sys.argv[3], "w") as f2:
        for line in open(sys.argv[1], "r"):
            line = line.split()[0]
            if line[0] == ">":
                first = not first
                if first:
                    block = []
                    f1.write(line + "\n")
                    f2.write(line + "\n")
                    n = 0
            else:
                if first:
                    block.append(line)
                else:
                    f1.write(line + "\n")
                    for i in range(len(line)):
                        f2.write(ambiguity[line[i] + block[n][i]])
                    f2.write("\n")
                    n += 1