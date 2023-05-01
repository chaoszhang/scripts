import sys

names = {}
for line in open(sys.argv[3], "r"):
    line = line.split()[0]
    names[line] = line

with open(sys.argv[2], "w") as f:
    for line in open(sys.argv[1], "r"):
        line = line.split()[0]
        if line[0] == ">":
            if line[1:] in names:
                f.write(line + "\n")
                used = True
            else:
                used = False
        else:
            if used:
                f.write(line + "\n")