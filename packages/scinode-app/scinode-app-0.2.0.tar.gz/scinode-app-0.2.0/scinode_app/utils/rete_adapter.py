class ReteAdaptor:
    """Adaptor serves as a bridge between SciNode and Rete."""

    @staticmethod
    def getScinodeDB(editor):
        """get SciNode data from a Rete Editor data,
        save the nodetree and all nodes to db.

        Args:
            nodetree (dict): _description_
            nodes (dict): _description_
        """
        import pickle

        nodes = {}
        alllinks = []
        for key, ndata in editor["nodes"].items():
            node = ndata.copy()
            # print("ndata: ", ndata)
            node["label"] = node["name"]
            node["name"] = str(node["id"])
            node["id"] = node["id"]
            node["meta"]["nodetree_uuid"] = editor["uuid"]
            if node["meta"]["daemon_name"] == "":
                node["meta"]["daemon_name"] = editor["meta"]["daemon_name"]
            # update properties
            # node['properties'] = node['controls']
            # update data
            node["properties"] = {}
            for key, value in ndata["data"].items():
                node["properties"][key] = {
                    "name": key,
                    "value": value,
                    "type": ndata["controls"][key]["type"],
                }
            # update inputs and outputs
            node["inputs"] = []
            for socket_name, link_data in ndata["inputs"].items():
                input = {
                    "link_limit": 1,
                    "links": [],
                    "name": socket_name,
                }
                links = []
                for connection in link_data["connections"]:
                    # data for nodetree
                    link = {
                        "from_node_name": str(connection["node"]),
                        "from_node_uuid": "",
                        "from_socket": connection["output"],
                    }
                    links.append(link)
                    alllinks.append(link)
                input["links"] = links
                node["inputs"].append(input)
            node["outputs"] = []
            for socket_name, link_data in ndata["outputs"].items():
                output = {
                    "class_name": "SocketFloatArgs",
                    "link_limit": 1,
                    "links": [],
                    "name": socket_name,
                }
                links = []
                for connection in link_data["connections"]:
                    # data for nodetree
                    link = {
                        "to_node_name": str(connection["node"]),
                        "to_node_uuid": "",
                        "to_socket": connection["input"],
                    }
                    links.append(link)
                    alllinks.append(link)
                output["links"] = links
                node["outputs"].append(output)
            node["properties"] = node["properties"]
            node["results"] = tuple(node["results"])
            node["outputs"] = node["outputs"]
            node["inputs"] = node["inputs"]
            # print('node: ', node)
            nodes[node["name"]] = node
            # insert_one(node, db['node'])
        #
        editor["version"] = editor.pop("id")
        editor["nodes"] = nodes
        print("nodetree: ", editor)
        return editor

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
        # print("getEditor: ", ntdata)
        editor["id"] = editor.pop("version")
        editor.pop("connectivity")
        editor_nodes = {}
        # print(nodes)
        for node_name, ndata in nodes.items():
            node = ndata.copy()
            # print("getEditor, ndata: ", ndata)
            # remove results
            node.pop("version", None)
            node.pop("results", None)
            node.pop("properties", None)
            # node.name => editor.node.id
            # node.meta.class_name => editor.node.name
            # node.label => editor.node.label
            node["id"] = int(node["id"])
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
            # print("properties: ", properties)
            node["data"] = {}
            for key, value in properties.items():
                node["data"][key] = value["value"]
            editor_nodes[node_name] = node
        #
        editor["nodes"] = editor_nodes
        print("editor: ", editor)
        return editor
