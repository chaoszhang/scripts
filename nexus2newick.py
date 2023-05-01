import sys
import re

with open(sys.argv[2], "w") as f:
    nameMap = {}
    isMapping = False
    for line in open(sys.argv[1], "r"):
        if isMapping:
            if line[0] == ";":
                isMapping = False
            else:
                e = line.split(",")[0].split()
                nameMap[e[0]] = e[1]
        if "Translate" in line:
            isMapping = True
        if line[0:4] == "tree":
            line = line.split("=", 1)[1]
            seq = [x for y in line.split("[") for x in y.split("]")]
            line = "".join([seq[i] for i in range(0, len(seq), 2)])
            line = re.sub(r':[^,);]*', "", line)
            line = re.split('([(,);])', line)
            line = [nameMap[e] if e in nameMap else e for e in line]
            f.write("".join(line).split()[0] + "\n")
            