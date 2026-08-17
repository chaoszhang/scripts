"""
# FastSplitAligner — README (embedded in source)

## License

This program is released under the MIT License.

MIT License

Copyright (c) 2026 Chao Zhang (ASTER LAB). This Python implementation is
copyrighted by Chao Zhang.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Provenance

Adapted from `compareTree.py` by Chao Zhang (ASTER LAB),
https://github.com/chaoszhang/scripts/blob/main/compareTree.py
Developed by WorkBuddy + DeepSeek under the guidance of Chao Zhang,
https://github.com/chaoszhang

The original SplitAligner tool (the Perl implementation and the branch
projection / NA-classification concept) is by Jiaqi Wu, Hiroshima University,
https://github.com/wujiaqi06/SplitAligner
This file is an independent Python implementation of the same idea; it does
not reuse any code from Jiaqi Wu's SplitAligner.pl.

The core branch-set mechanism (random 512-bit leaf hashes, subtree hash
summation, and complement-equivalence via `min(h, root-h)`) is taken directly
from `compareTree.py`. SplitAligner extends it from a tree-vs-tree RF tool
into a species-tree x gene-tree branch mapping and NA classification tool.

## Why the branch-set method is correct

Every branch of an unrooted tree is a bipartition of its leaf set. We encode
each leaf set `S` by `h(S) = sum over x in S of r(x)` over the ring `Z/2^512`,
where `r(x)` is a uniform random 512-bit value assigned once per taxon.

1. **Uniformity.** `r(x) = (a ^ b) + c` with independent uniform `a, b, c`:
   XOR keeps uniformity in the Abelian group, and modular addition convolves
   uniform with uniform, which is again uniform on `Z/2^512`.
2. **Collision-freeness.** If `S != T` then `h(S) - h(T)` is a sum of an
   odd number of independent uniform group elements, hence uniform, hence
   `h(S) == h(T)` with probability `2^-512`. Practically impossible.
3. **Direction elimination.** A bipartition `A|B` is unordered; we compare
   `min(h(A), h(B))` with `B = L - A`, so both orientations collapse to one
   key. Since `h` is a true group sum, `h(B) = h(L) - h(A)` exactly (no
   floating-point error), so the min-complement trick is exact, not
   approximate.

Therefore "same hash key" is equivalent to "same leaf set" for all practical
purposes, which is exactly what branch identity requires.

## Why it is fast

1. Per tree, hashing is one addition per node: `O(n)` total, versus `O(n^2)`
   for bipartition-string-set comparisons.
2. Per gene, the projected hash `h(A ∩ L_G)` for every species-tree branch
   is obtained by a single postorder pass over the species tree, where a
   species leaf absent from `L_G` contributes hash 0:
   `O(|L_S|)` additions, independent of the gene size and the tree shape.
3. Every lookup (branch key to gene branch length, fuse counting) is a
   `dict` operation, `O(1)` expected.
4. Result: 2275 genes x 302 taxa run in ~5.6 s in pure Python with no external
   dependencies.

## NA classification: pseudocode

For species-tree branch `A|B` and a gene with leaf set `L_G`:

```
A' = A ∩ L_G;  B' = B ∩ L_G
if h(A') == 0 or h(A') == h(L_G):    # i.e. |A'| == 0 or |B'| == 0
    -> NA_struct            # a projected side vanished
else:
    key = min(h(A'), h(L_G) - h(A'))
    fuse = (count of species-tree branches projecting to key) > 1
    topo = (key not in the gene tree's split set)
    if fuse and topo:  -> NA_fuse_topo
    elif fuse:         -> NA_fuse
    elif topo:         -> NA_topo
    else:
        if the matching gene branch has no length: -> NA_len
        else:                                      -> the branch length
```

`NA_struct` is checked first: when a projected side is empty the branch has
no projected identity at all, so neither fuse nor topo is well defined.

## Why topo and fuse are orthogonal

- **fuse** is a property of the *species-tree side*: the projection map
  (species branch -> induced split) fails to be injective — two or more
  distinct species-tree branches collapse onto the same induced split.
- **topo** is a property of the *gene-tree side*: the induced split exists
  nowhere in the gene tree.

They are independent axes: a split can be multiply mapped yet present
(fuse only), uniquely mapped yet absent (topo only), multiply mapped and
absent (both: NA_fuse_topo), or uniquely mapped and present (numeric). Hence
the 2 x 2 combination is the complete, non-redundant classification, and
merging fuse+topo into one of the two (as the original implementation did)
loses one axis of biological information.

## Input / output summary

Input:
  species.nwk   one unrooted binary species tree (Newick; lengths/labels ignored)
  genes.nwk     one gene tree per line: `gene_name(Newick)`; internal labels
                ignored, branch lengths kept; gene leaf set ⊆ species leaf set

Output:
  <prefix>.tre  annotated species tree: internal nodes labeled `B<number>`
                (internal branches numbered consecutively B1..B299 in postorder,
                skipping terminal branches); the root is unlabeled; for a
                binary root the two children share the same label (they are
                complementary sides of one unrooted branch)
  <prefix>.tsv  table: gene (input order) x 601 branches (2n-3) in postorder;
                terminal branches use species names, internal branches B1..B299
"""


import sys
import re
import random
from decimal import Decimal

sys.setrecursionlimit(100000)

MAXRAND = 2 ** 512


def random_leaf_hash():
    # Same as compareTree: uniform on the additive group mod 2^512
    return (random.randrange(MAXRAND) ^ random.randrange(MAXRAND)) + random.randrange(MAXRAND)


# ---------------- Newick parsing (internal labels ignored, raw lengths kept) ----------------

def parse_newick(s):
    tokens = [t for t in re.split(r"([(,:);])", s) if t]
    root, i = _parse_node(tokens, 0, None)
    return root


def _parse_node(tokens, i, parent):
    node = {"children": [], "parent": parent, "leaf": False, "label": None, "bl": None}
    if tokens[i] == "(":
        child, i = _parse_node(tokens, i + 1, node)
        node["children"].append(child)
        while tokens[i] != ")":
            # tokens[i] must be ','
            child, i = _parse_node(tokens, i + 1, node)
            node["children"].append(child)
        i += 1  # skip ')'
        # internal node suffix: [label] [:len]
        if tokens[i] == ":":
            node["bl"] = tokens[i + 1]
            i += 2
        elif tokens[i] not in ",();":
            i += 1  # skip internal label
            if tokens[i] == ":":
                node["bl"] = tokens[i + 1]
                i += 2
    else:
        node["leaf"] = True
        node["label"] = tokens[i]
        i += 1
        if tokens[i] == ":":
            node["bl"] = tokens[i + 1]
            i += 2
    return node, i


# ---------------- Species tree: postorder node list + branch sequence ----------------

def build_species(species_newick):
    root = parse_newick(species_newick)
    nodes = []          # postorder (root included, root last)
    leaf_by_name = {}

    def post(n):
        for c in n["children"]:
            post(c)
        nodes.append(n)
        if n["leaf"]:
            leaf_by_name[n["label"]] = n

    post(root)
    for i, n in enumerate(nodes):
        n["idx"] = i
    root["idx"] = len(nodes) - 1

    # Branch sequence (2n-3 entries): all non-root nodes in postorder.
    # Binary root: the two children's clades are complementary sides of one
    # unrooted branch, so keep only one (the leaf if present, else the first
    # child in postorder).
    # Trifurcating root (standard unrooted serialization): the three children
    # each define an independent unrooted branch; keep all of them.
    seq = list(nodes)
    seq.pop()  # drop the root
    drop = None
    keep = None
    if len(root["children"]) == 2:
        u, v = root["children"]  # v is the later child in postorder
        if u["leaf"]:
            keep, drop = u, v
        elif v["leaf"]:
            keep, drop = v, u
        else:
            keep, drop = u, v
        for i, n in enumerate(seq):
            if n is drop:
                del seq[i]
                break
    return root, nodes, leaf_by_name, seq, keep, drop


# ---------------- Annotated species tree output ----------------

def to_newick(n, label_of):
    if n["leaf"]:
        return n["label"]
    inner = "(" + ",".join(to_newick(c, label_of) for c in n["children"]) + ")"
    lab = label_of.get(id(n))
    return inner + lab if lab else inner


# ---------------- Main workflow ----------------

def main():
    if len(sys.argv) != 4:
        print("usage: python splitAligner.py species.nwk genes.nwk out_prefix", file=sys.stderr)
        sys.exit(1)

    species_file, genes_file, out_prefix = sys.argv[1:]

    # ---- species tree ----
    sp_root, sp_nodes, leaf_by_name, seq, keep, drop = build_species(
        open(species_file, encoding="utf-8").readline().strip())

    # leaf hashes (global, shared by species tree and gene trees)
    sp_hash = {name: random_leaf_hash() for name in leaf_by_name}

    # column names: terminal branches use species names; internal branches use
    # consecutive B numbers (B1.., numbered independently of terminal branches)
    col_names = []
    label_of = {}
    internal_counter = 0
    for pos, n in enumerate(seq):
        if n["leaf"]:
            col_names.append(n["label"])
        else:
            internal_counter += 1
            bname = "B%d" % internal_counter
            col_names.append(bname)
            label_of[id(n)] = bname
    if drop is not None and not drop["leaf"]:
        # binary root: both children carry the same label
        kp = keep if keep is not None else seq[0]
        kp_name = None
        for n, nm in zip(seq, col_names):
            if n is kp:
                kp_name = nm
                break
        label_of[id(drop)] = kp_name

    # write annotated species tree
    tre_str = to_newick(sp_root, label_of)
    with open(out_prefix + ".tre", "w", encoding="utf-8") as f:
        f.write(tre_str + ";\n")

    # ---- per-gene processing ----
    with open(out_prefix + ".tsv", "w", encoding="utf-8") as f:
        f.write("\t".join(["gene"] + col_names) + "\n")
        ngenes = 0
        for line in open(genes_file, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            gname = line[:line.index("(")]
            gtree = parse_newick(line[line.index("("):])

            # gene tree postorder + subtree hash sums (leaves absent from the
            # species tree contribute 0)
            g_nodes = []

            def gpost(n):
                if n["leaf"]:
                    h = sp_hash.get(n["label"], 0)
                else:
                    h = 0
                    for c in n["children"]:
                        h += gpost(c)
                n["h"] = h
                g_nodes.append(n)
                return h

            gpost(gtree)
            H_G = gtree["h"]

            # gene tree split -> length dict (complementary root children are the
            # two halves of one unrooted branch, so their lengths are summed)
            gdict = {}
            for n in g_nodes:
                if n is gtree:
                    continue
                h = n["h"]
                key = min(h, H_G - h)
                bl = n["bl"]
                if key in gdict:
                    prev_h, prev_bl = gdict[key]
                    if prev_h == H_G - h:  # complementary pair: sum the two halves
                        if bl is None or prev_bl is None:
                            gdict[key] = (h, None)
                        else:
                            gdict[key] = (h, str(Decimal(prev_bl) + Decimal(bl)).lower())
                    # otherwise a hash collision (probability ~2^-512): overwrite
                else:
                    gdict[key] = (h, bl)

            # projected hashes: one postorder pass over the species tree, O(|L_S|).
            # A species leaf absent from the gene contributes hash 0, so a node's
            # hash is h(A ∩ L_G) for its clade A (children precede parents in
            # sp_nodes, which is postorder).
            gene_set = {n["label"] for n in g_nodes if n["leaf"]}
            ghash = [0] * len(sp_nodes)
            for n in sp_nodes:
                if n["leaf"]:
                    ghash[n["idx"]] = sp_hash[n["label"]] if n["label"] in gene_set else 0
                else:
                    ghash[n["idx"]] = 0
                    for c in n["children"]:
                        ghash[n["idx"]] += ghash[c["idx"]]
            assert ghash[sp_root["idx"]] == H_G, "hash mismatch"

            # species branches -> projected keys, fuse detection
            keys = []
            for n in seq:
                h = ghash[n["idx"]]
                if h == 0 or h == H_G:
                    keys.append(None)  # struct: a projected side is empty
                else:
                    keys.append(min(h, H_G - h))

            from collections import Counter
            cnt = Counter(k for k in keys if k is not None)
            fuse_keys = {k for k, c in cnt.items() if c > 1}

            row = [gname]
            for n, key in zip(seq, keys):
                if key is None:
                    row.append("NA_struct")
                    continue
                fuse = key in fuse_keys
                topo = key not in gdict
                if fuse and topo:
                    row.append("NA_fuse_topo")
                elif fuse:
                    row.append("NA_fuse")
                elif topo:
                    row.append("NA_topo")
                else:
                    bl = gdict[key][1]
                    row.append(bl if bl is not None else "NA_len")
            f.write("\t".join(row) + "\n")
            ngenes += 1

    print("done: %s.tre, %s.tsv (%d genes)" % (out_prefix, out_prefix, ngenes))


if __name__ == "__main__":
    main()
