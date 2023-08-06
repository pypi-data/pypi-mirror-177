class ReteAdaptor:
    """Adaptor serves as a bridge between Xnodes and Rete."""

    @staticmethod
    def getEditor(query, db, is_template=False):
        """Load data from database, and change to Editor format.

        Args:
            record (mongodb cursor): _description_
            db (_type_): _description_

        Returns:
            dict: _description_
        """
        import pickle

        # print(query)
        if is_template:
            db_nodetree_name = "template_nodetree"
            db_node_name = "template_node"
        else:
            db_nodetree_name = "nodetree"
            db_node_name = "node"
        ntdata = db[db_nodetree_name].find_one(query, {"_id": 0})
        # fetch node data
        nodes = {}
        for key, data in ntdata["nodes"].items():
            ndata = db[db_node_name].find_one({"uuid": data["uuid"]}, {"_id": 0})
            nodes[key] = ndata
        editor = ntdata.copy()
        editor_nodes = {}
        # print(nodes)
        for node_name, ndata in nodes.items():
            node = ndata.copy()
            # remove results
            del node["results"]
            del node["properties"]
            # node.name => editor.node.id
            # node.meta.class_name => editor.node.name
            # node.label => editor.node.label
            node["id"] = node["name"]
            node["name"] = node["meta"]["class_name"]
            # inputs
            node["inputs"] = {}
            inputs = ndata["inputs"]
            for input in inputs:
                if input["name"] not in node["inputs"]:
                    node["inputs"][input["name"]] = {"connections": []}
                for link in input["links"]:
                    connection = {
                        "node": link["from_node_name"],
                        "output": link["from_socket"],
                        "data": {},
                    }
                    node["inputs"][input["name"]]["connections"].append(connection)
            # ouputs
            outputs = ndata["outputs"]
            node["outputs"] = {}
            for output in outputs:
                if output["name"] not in node["outputs"]:
                    node["outputs"][output["name"]] = {"connections": []}
                for link in output["links"]:
                    connection = {
                        "node": link["to_node_name"],
                        "input": link["to_socket"],
                        "data": {},
                    }
                    node["outputs"][output["name"]]["connections"].append(connection)
            # properties to data
            properties = pickle.loads(ndata["properties"])
            print("properties: ", properties)
            node["data"] = {}
            for key, value in properties.items():
                node["data"][key] = value["value"]
            editor_nodes[node_name] = node
        #
        editor["nodes"] = editor_nodes
        # print("editor: ", editor)
        return editor
