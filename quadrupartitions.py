import dendropy
import sys

cnt = 0
leafset = []

def get_quadripartitions(tree, u, v, is_root = False):
    global cnt
    global leafset
    if u.is_internal():
        u1, u2 = u.child_nodes()
        get_quadripartitions(tree, u1, u2)
        if not is_root:
            leaves1 = u1.leaf_nodes()
            leaves2 = u2.leaf_nodes()
            leaves3 = v.leaf_nodes()
            leaves1_names = [leaf.taxon.label for leaf in leaves1]
            leaves2_names = [leaf.taxon.label for leaf in leaves2]
            leaves3_names = [leaf.taxon.label for leaf in leaves3]
            leaves4_names = [leaf for leaf in leafset if leaf not in leaves1_names and leaf not in leaves2_names and leaf not in leaves3_names]
            cnt += 1
            u.label = str(cnt)
            with open("sliding/" + str(cnt) + "/mapping", "w") as f:
                for leaf in leaves1_names:
                    f.write(leaf.replace(" ", "_") + "\tA\n")
                for leaf in leaves2_names:
                    f.write(leaf.replace(" ", "_") + "\tB\n")
                for leaf in leaves3_names:
                    f.write(leaf.replace(" ", "_") + "\tC\n")
                for leaf in leaves4_names:
                    f.write(leaf.replace(" ", "_") + "\tD\n")
        get_quadripartitions(tree, u2, u1)
               
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <newick_file_path>")
        sys.exit(1)

    newick_file_path = sys.argv[1]
    tree = dendropy.Tree.get(path=newick_file_path, schema="newick")
    leafset = [leaf.taxon.label for leaf in tree.leaf_node_iter()]
    get_quadripartitions(tree, tree.seed_node.child_nodes()[0], tree.seed_node.child_nodes()[1], is_root = True)
    get_quadripartitions(tree, tree.seed_node.child_nodes()[1], tree.seed_node.child_nodes()[0], is_root = True)
    print(tree.as_string("newick"))