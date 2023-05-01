import sys

na2aa = { "TTT":"F", "TTC":"F", "TTA":"L", "TTG":"L", "CTT":"L", "CTC":"L", "CTA":"L", "CTG":"L", "ATT":"I", "ATC":"I", "ATA":"I", "ATG":"M", "GTT":"V", "GTC":"V", "GTA":"V", "GTG":"V", "TCT":"S", "TCC":"S", "TCA":"S", "TCG":"S", "CCT":"P", "CCC":"P", "CCA":"P", "CCG":"P", "ACT":"T", "ACC":"T", "ACA":"T", "ACG":"T", "GCT":"A", "GCC":"A", "GCA":"A", "GCG":"A", "TAT":"Y", "TAC":"Y", "TAA":"*", "TAG":"*", "CAT":"H", "CAC":"H", "CAA":"Q", "CAG":"Q", "AAT":"N", "AAC":"N", "AAA":"K", "AAG":"K", "GAT":"D", "GAC":"D", "GAA":"E", "GAG":"E", "TGT":"C", "TGC":"C", "TGA":"*", "TGG":"W", "CGT":"R", "CGC":"R", "CGA":"R", "CGG":"R", "AGT":"S", "AGC":"S", "AGA":"R", "AGG":"R", "GGT":"G", "GGC":"G", "GGA":"G", "GGG":"G" } 

cnt = 0
with open(sys.argv[2], "w") as f:
    for line in open(sys.argv[1], "r"):
        line = line.split()
        if cnt == 0:
            cnt = int(line[0])
            f.write(line[0] + "\t" + str(int(int(line[1]) / 3)) + "\n")
        else:
            f.write(line[0] + "\t" + "".join([na2aa[line[1][3*i:3*i+3]] if line[1][3*i:3*i+3] in na2aa else "-" for i in range(int(len(line[1]) / 3))]) + "\n")
            cnt -= 1