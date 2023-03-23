import sys

def newick(f, lines, i, j):
    while lines[i][j] == "-":
        j = j + 1
    if lines[i][j] == "+":
        f.write("(")
        i0 = i - 1
        while lines[i0][j] == "|":
            i0 = i0 - 1
        newick(f, lines, i0, j + 1)
        f.write(",")
        i1 = i + 1
        while lines[i1][j] == "|":
            i1 = i1 + 1
        newick(f, lines, i1, j + 1)
        f.write(")")
    else:
        f.write(lines[i][j+1:].split()[0])

lines = []
for line in open(sys.argv[1], "r"):
    lines.append(line)
with open(sys.argv[2], "w") as f:
    f.write("(")
    for i in range(len(lines)):
        if len(lines[i]) > 0 and lines[i][0] == "/":
            newick(f, lines, i, 1)
            break
    f.write(",")
    for i in range(len(lines)):
        if len(lines[i]) > 0 and lines[i][0] == "\\":
            newick(f, lines, i, 1)
            break
    f.write(");\n")