def build_nodetree_python_script(ntdata, nodes):
    import pickle

    print("ntdata: ", ntdata)
    s = """
from scinode.nodetree import NodeTree
nt = NodeTree(name="{}")
""".format(
        ntdata["name"]
    )
    # nodes
    for node in nodes:
        print("node: ", node)
        s += """
node = nt.nodes.new("{}", "{}")
""".format(
            node["meta"]["class_name"], node["label"]
        )
        # set node properties
        properties = pickle.loads(node["properties"])
        for name, p in properties.items():
            print("\np: ", p)
            if p["value"] == "":
                continue
            if p["type"] in ["String", "Enum"]:
                s += """
node.properties["{}"].value = "{}"
    """.format(
                    p["name"], p["value"]
                )
            else:
                s += """
node.properties["{}"].value = {}
    """.format(
                    p["name"], p["value"]
                )

    # links
    for link in ntdata["links"]:
        s += """
nt.links.new(nt.nodes["{}"].outputs["{}"], nt.nodes["{}"].inputs["{}"])
""".format(
            link["from_node_name"],
            link["from_socket"],
            link["to_node_name"],
            link["to_socket"],
        )

    # launch
    s += """
nt.launch()
"""
    return s
