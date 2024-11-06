import sys

alignment = []
for line in open(sys.argv[1]):
    line = line.split()
    if len(line) == 0 or (line[0] != "a" and line[0][0] != "s"):
        continue
    if line[0][0] == "a":
        if len(alignment) >= 4:
            print(len(alignment), len(alignment[0][1]))
            for e in alignment:
                print(e[0], e[1])
        alignment = []
    elif int(line[3]) > 100:
        alignment.append((line[1], line[6]))