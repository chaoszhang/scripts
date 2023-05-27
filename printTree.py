import dendropy
import sys

def get_quadripartitions(tree):
    quadripartitions = []
    for w in tree.preorder_node_iter():
        if w == tree.seed_node:
            continue
        if w.is_internal():
            u, v = w.child_nodes()
            if u.is_internal():
                u1, u2 = u.child_nodes()
                quadripartitions.append((u1.leaf_nodes(), u2.leaf_nodes(), v.leaf_nodes()))
            if v.is_internal():
                v1, v2 = v.child_nodes()
                quadripartitions.append((v1.leaf_nodes(), v2.leaf_nodes(), u.leaf_nodes()))
    return quadripartitions

tree = dendropy.Tree.get(path=sys.argv[1], schema="newick")
i = 0
for w in tree.preorder_node_iter():
    if w == tree.seed_node:
        continue
    if w.is_internal():
        u, v = w.child_nodes()
        if u.is_internal():
            i += 1
            u.label = str(i)
        if v.is_internal():
            i += 1
            v.label = str(i)
print(tree.as_string("newick"))