import sys

lines = open(sys.argv[1], "r").readlines()
realnames = lines[0].split()
ploidy = [len([c for s in seq.split("/") for c in s.split("|") ]) for seq in lines[1].split()]
names = [realnames[i] for i in range(len(realnames)) for k in range(ploidy[i])]
with open(sys.argv[2], "w") as f:
    for i in range(len(names)):
        f.write(">" + names[i] + "\n")
        for j in range(len(lines) - 1):
            f.write(lines[j + 1][2 * i])
        f.write("\n")