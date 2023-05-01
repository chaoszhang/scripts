import sys

with open(sys.argv[2], "w") as f:
    for line in open(sys.argv[1], "r"):
        if line[0] == ">":
            f.write(line)
        else:
            f.write("".join([line[i] for i in range(len(line)) if i % 3 != 2]))