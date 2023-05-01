import sys

aa2na = {
    "C":"A",
    "S":"C","T":"C","A":"C","G":"C","P":"C",
    "D":"T","E":"T","Q":"T","N":"T",
    "H":"T","R":"T","K":"T",
    "M":"A","I":"A","L":"A","V":"A",
    "W":"G","Y":"G","F":"G"
}

cnt = 0
with open(sys.argv[2], "w") as f:
    for line in open(sys.argv[1], "r"):
        line = line.split()
        if cnt == 0:
            cnt = int(line[0])
            f.write(line[0] + "\t" + line[1] + "\n")
        else:
            f.write(line[0] + "\t" + "".join([aa2na[c] if c in aa2na else c for c in line[1]]) + "\n")
            cnt -= 1