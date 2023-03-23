import sys

aa2na = {
    "C":"A",
    "S":"C","T":"C","A":"C","G":"C","P":"C",
    "D":"T","E":"T","Q":"T","N":"T",
    "H":"T","R":"T","K":"T",
    "M":"A","I":"A","L":"A","V":"A",
    "W":"G","Y":"G","F":"G"
}

with open(sys.argv[2], "w") as f:
    for line in open(sys.argv[1], "r"):
        if line[0] == ">":
            f.write(line)
        else:
            f.write("".join([aa2na[c] if c in aa2na else c for c in line]))