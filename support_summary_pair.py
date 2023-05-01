import sys

for line in open(sys.argv[1], "r"):
    line = line.split("'")
    for i in range(1, len(line), 2):
        s = line[i]
        s = s[5:-1].split(";")
        bs1 = int(s[0])
        s1 = float(s[3].split("=")[1])
        s2 = float(s[4].split("=")[1])
        s3 = float(s[5].split("=")[1])
        total = s1 + s2 + s3
        line[i] = str(round(0.1 * bs1, 1)) + "/" + str(round((s1 - max(s2, s3)) / (s1 - min(s2, s3)), 3))
        
    print("".join(line))