import sys
import math

chrn = [str(j) for j in range(1, 23)] + ["X"]
s1 = [[float('nan') for j in range(23)] for i in range(239)]
s2 = [[float('nan') for j in range(23)] for i in range(239)]
s3 = [[float('nan') for j in range(23)] for i in range(239)]

for j in range(23):
    i = -2
    for line in open("chr/" + chrn[j] + "/chr" + chrn[j] + ".site.compareTrees", "r"):
        i += 1
        line = line.split("'")
        if len(line) != 3:
            continue
        
        s = line[1]
        s = s[5:-1].split(";")
        bs1 = int(s[0])
        s1[i][j] = float(s[3].split("=")[1])
        s2[i][j] = float(s[4].split("=")[1])
        s3[i][j] = float(s[5].split("=")[1])
            
titleline = "\t".join(chrn) + "\n"

with open("stat/s1.tsv", "w") as f:
    f.write(titleline)
    for i in range(239):
        f.write("\t".join(str(s1[i])) + "\n")

with open("stat/s2.tsv", "w") as f:
    f.write(titleline)
    for i in range(239):
        f.write("\t".join(str(s2[i])) + "\n")

with open("stat/s3.tsv", "w") as f:
    f.write(titleline)
    for i in range(239):
        f.write("\t".join(str(s3[i])) + "\n")

chrTotal = [0 for j in range(23)]
chrTotal[5-1] = 113328470.121704+112875867.382952+97103125.646248
chrTotal[7-1] = 117935.607546+113096.555387+117193.396356
chrTotal[13-1] = 46535619.273174+44745191.231040+35530982.978932
chrTotal[16-1] = 103977.098775+97807.894844+99610.200288
chrTotal[17-1] = 14811.363361+10062.722682+14180.276981
chrTotal[18-1] = 62940.527990+57549.997561+60954.360883
chrTotal[19-1] = 9820.097174+5948.431946+9214.990206 + 98729.367137+69033.203301+97415.089209 + 18351.464899+14342.640935+9207.640011 + 29296.036788+27784.909087+18281.084690
chrTotal[22-1] = 8616.561346+5983.159273+7795.675203 + 15168.381503+13937.848195+10480.203142
chrTotal[23-1] = 68674104.980655+63619208.054766+61347740.238163 + 81204.921769+68958.776427+70824.886183
for i in range(239):
    for j in range(23):
        if not math.isnan(s1[i][j]):
            chrTotal[j] += s1[i][j] + s2[i][j] + s3[i][j]

with open("stat/signal.tsv", "w") as f:
    f.write(titleline)
    for i in range(239):
        row = [(s1[i][j] + s2[i][j] + s3[i][j]) / chrTotal[j] for j in range(23)]
        valid = [v for v in row if not math.isnan(v)]
        avg = sum(valid) / len(valid)
        f.write("\t".join([str(row[j] / avg) for j in range(23)]) + "\n")

with open("stat/major.tsv", "w") as f:
    f.write(titleline)
    for i in range(239):
        row = [s1[i][j] / (s1[i][j] + s2[i][j] + s3[i][j]) for j in range(23)]
        valid = [v for v in row if not math.isnan(v)]
        avg = sum(valid) / len(valid)
        f.write("\t".join([str(row[j] / avg) for j in range(23)]) + "\n")

with open("stat/hgt.tsv", "w") as f:
    f.write(titleline)
    for i in range(239):
        row = [abs(s2[i][j] - s3[i][j]) / (s1[i][j] + s2[i][j] + s3[i][j]) for j in range(23)]
        valid = [v for v in row if not math.isnan(v)]
        avg = sum(valid) / len(valid)
        f.write("\t".join([str(row[j] / avg) for j in range(23)]) + "\n")
