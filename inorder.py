import sys
import re

def parseNewickHelper(nw, i, p):
    cur = {"P": p, "isroot": p is None}
    if nw[i] == "(":
        LC, i = parseNewickHelper(nw, i + 1, cur)
        while nw[i] != ",":
            i += 1
        RC, i = parseNewickHelper(nw, i + 1, cur)
        while nw[i] != ")":
            i += 1
        if nw[i + 1] not in ":),;":
            i += 1
            cur["label"] = nw[i]
        cur["LC"] = LC
        cur["RC"] = RC
        cur["isleaf"] = False
    else:
        cur["label"] = nw[i]
        cur["isleaf"] = True
    i += 1
    while nw[i] not in ":,);":
        i += 1
    if nw[i] == ":":
        i += 1
        cur["length"] = nw[i]
        while nw[i] not in ",);":
            i += 1
    return cur, i

def parseNewick(nw):
    tree = parseNewickHelper([e for e in re.split("([(,:);])", nw) if e != ""], 0, None)[0]
    return tree

def printNewick(node):
    if node["isleaf"]:
        return node["label"]
    else:
        return "(" + printNewick(node["LC"]) + "," + printNewick(node["RC"]) + ")" + (node["label"] if "label" in node else "")

def printLeaves(node):
    if node["isleaf"]:
        return '"' + node["label"] + '"'
    else:
        if "label" in node:
            return printLeaves(node["LC"]) + "," + '"' + node["label"] + '"' + "," + printLeaves(node["RC"])
        else:
            return printLeaves(node["LC"]) + "," + printLeaves(node["RC"])

tree = parseNewick(sys.stdin.readline())
print(printNewick(tree) + ";")
print(printLeaves(tree))