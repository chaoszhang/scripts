import sys

block = []
first = False
n = 0

ambiguity = {
    "A":"AA", "M":"AC", "R":"AG", "W":"AT",
    "M":"CA", "C":"CC", "S":"CG", "Y":"CT",
    "R":"GA", "S":"GC", "G":"GG", "K":"GT",
    "W":"TA", "Y":"TC", "K":"TG", "T":"TT"
}

name = ""
seq = []
for line in open(sys.argv[1], "r"):
    line = line.split()[0]
    if line[0] == ">":
        if name != "":
            seq = "".join(seq)
            print(name)
            print("".join([ambiguity[c][0] if c in ambiguity else "N" for c in seq]))
            print(name)
            print("".join([ambiguity[c][1] if c in ambiguity else "N" for c in seq]))
        name = line
        seq = []
    else:
        seq.append(line)
if name != "":
    seq = "".join(seq)
    print(name)
    print("".join([ambiguity[c][0] if c in ambiguity else "N" for c in seq]))
    print(name)
    print("".join([ambiguity[c][1] if c in ambiguity else "N" for c in seq]))