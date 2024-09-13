import sys, re, secrets, argparse, warnings
import numpy as np

LEN = 4

def randomElement():
    return np.asarray([int(secrets.token_hex(8), 16) for i in range(LEN)], dtype=np.uint64)

def identityElement():
    return np.zeros(LEN, dtype=np.uint64)

def elementEqual(a, b):
    return np.array_equal(a, b)

def string2label(s):
    a = s.split(":")
    if len(a) == 1:
        return {"label": a[0], "length": ""}
    else:
        return {"label": a[0], "length": a[1]}

def token2subtree(a, i):
    children = []
    while i < len(a) and a[i] == "":
        i += 1
    if a[i] == "(":
        while a[i] != ")":
            c, i = token2subtree(a, i + 1)
            children.append(c)
            while i < len(a) and a[i] == "":
                i += 1
        i += 1
    d = string2label(a[i] if i < len(a) else "")
    return ({"children": children, "label": d["label"], "length": d["length"]}, i + 1)

def string2tree(s):
    a = re.split("([(,)])", s)
    return token2subtree(a, 0)[0]

def buildRecursion(node, tree):
    if len(node["children"]) == 0:
        if node["label"] in tree["label2leaf"]:
            print("Duplicated leaves?")
            exit(1)
        tree["label2leaf"][node["label"]] = node
        e = randomElement()
    else:
        e = identityElement()
        for child in node["children"]:
            buildRecursion(child, tree)
            e += child["element"]
    node["element"] = e
    h = e[0]
    if h in tree["hash2node"]:
        print("Unlucky, try again!")
        exit(1)
    tree["hash2node"][h] = node
    
def buildTree(root):
    tree = {"root": root, "label2leaf": {}, "hash2node": {}}
    buildRecursion(root, tree)
    return tree

def mapRecursion(node, tree, ref):
    if len(node["children"]) == 0:
        if node["label"] in tree["label2leaf"]:
            print("Duplicated leaves?")
            exit(1)
        tree["label2leaf"][node["label"]] = node
        e = ref["label2leaf"][node["label"]]["element"]
    else:
        e = identityElement()
        for child in node["children"]:
            mapRecursion(child, tree, ref)
            e += child["element"]
    node["element"] = e
    h = e[0]
    if h in tree["hash2node"]:
        print("Unlucky, try again!")
        exit(1)
    tree["hash2node"][h] = node

def mapTree(root, ref):
    tree = {"root": root, "label2leaf": {}, "hash2node": {}}
    mapRecursion(root, tree, ref)
    return tree

def missingBranch(query, ref):
    cnt = 0
    s = ref["root"]["element"]
    keynodeH = query["root"]["children"][0]["element"][0] if len(query["root"]["children"]) == 2 else 0
    for h in query["hash2node"]:
        if h == keynodeH:
            continue
        if h in ref["hash2node"]:
            if not elementEqual(query["hash2node"][h]["element"], ref["hash2node"][h]["element"]):
                print("Unlucky, try again!")
                exit(1)
        elif s[0] - h in ref["hash2node"]:
            if not elementEqual(s - query["hash2node"][h]["element"], ref["hash2node"][s[0] - h]["element"]):
                print("Unlucky, try again!")
                exit(1)
        else:
            cnt += 1
    return cnt


with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    with open(sys.argv[1]) as file1:
        root = string2tree(file1.readline().split(";")[0])
        tree = buildTree(root)
    for i in range(2, len(sys.argv)):
        with open(sys.argv[i]) as file2:
            root2 = string2tree(file2.readline().split(";")[0])
            tree2 = mapTree(root2, tree)
        print(missingBranch(tree, tree2))