import sys

cnt = 0
with open(sys.argv[2], "w") as f:
    for line in open(sys.argv[1], "r"):
        line = line.split()
        if cnt == 0:
            cnt = int(line[0])
            f.write(line[0] + "\t" + str(int(int(line[1]) * 2 / 3)) + "\n")
        else:
            f.write(line[0] + "\t" + "".join([line[1][i] for i in range(len(line[1])) if i % 3 != 2]) + "\n")
            cnt -= 1