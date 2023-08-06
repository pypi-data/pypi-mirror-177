from scinode_app.core.rete_adapter import ReteAdaptor


class NodeTree:
    """Build nodetree from Rete Editor data"""

    def __init__(self, editor, db) -> None:
        """_summary_

        Args:
            name (str, optional): name of the nodetree.
                Defaults to "NodeTree".
            type (str, optional): type of the nodetree.
                This should be the same of the name of the Class.
                Defaults to "NodeTree".
            uuid (str, optional): uuid of the nodetree.
                Defaults to None.
            daemon_name (str, optional): name of the daemon.
                Defaults to "localhost".
            parent (str, optional): uuid of the parent nodetree.
                Defaults to ''.
        """
        self.nodetree, self.nodes = NodeTree.getScinodeDB(editor)
        self.db = db

    def saveNodetree(self):
        """Save Nodetree
        Check the uuid first.
        If uuid exist, update the nodetree in the database
        If uuid not exit, create a new nodetree in
        the database

        Args:
            nodetree (_type_): _description_
            nodes (_type_): _description_
        """
        self.initNodetree()
        for name, node in self.nodes.items():
            self.updateNode(node)
        self.updateNodetree()

    def launchNodetree(self):
        """Launch Nodetree
        Check the uuid first.
        If uuid exist, update the nodetree in the database
        If uuid not exit, create a new nodetree in
        the database

        Args:
            nodetree (_type_): _description_
            nodes (_type_): _description_
        """
        self.initNodetree()
        for name, node in self.nodes.items():
            if node["state"] == "FINISHED":
                continue
            node["action"] = "LAUNCH"
            self.updateNode(node)
        self.nodetree["action"] = "LAUNCH"
        self.updateNodetree()

    def initNodetree(self):
        """Create a new nodetree in database

        step 1: assign uuid to nodetree
        step 2: assign uuid and nodetree_uuid to nodes
        step 3: init to db

        Args:
            nodetree (_type_): _description_
            nodes (_type_): _description_
        """
        from scinode.utils.node import insert_one
        import uuid

        # assign uuid to nodetree
        if self.nodetree["uuid"] == "":
            self.nodetree["uuid"] = str(uuid.uuid4())
            self.nodetree["state"] = "CREATED"
            insert_one(self.nodetree, self.db["nodetree"])
        # add uuid for node
        self.initNodes()
        links = []
        # update uuid for links
        for name, node in self.nodes.items():
            self.nodetree["nodes"][name]["uuid"] = node["uuid"]
            for input in node["inputs"]:
                for link in input["links"]:
                    link["from_node_uuid"] = self.nodes[link["from_node_name"]]["uuid"]
                    full_link = link.copy()
                    full_link["to_node_uuid"] = node["uuid"]
                    full_link["to_node_name"] = node["name"]
                    full_link["to_socket"] = input["name"]
                    links.append(full_link)
        # update uuid for links
        for name, node in self.nodes.items():
            for output in node["outputs"]:
                for link in output["links"]:
                    link["to_node_uuid"] = self.nodes[link["to_node_name"]]["uuid"]
        self.nodetree["links"] = links

    def initNodes(self):
        """Create a new Node in database

        Args:
            node (_type_): _description_
        """
        from scinode.utils.node import insert_one
        import uuid

        for name, node in self.nodes.items():
            node["meta"]["nodetree_uuid"] = self.nodetree["uuid"]
            if node["uuid"] == "":
                node["uuid"] = str(uuid.uuid4())
                node["state"] = "CREATED"
                insert_one(node, self.db["node"])

    def updateNode(self, node):
        """Update a node

        Args:
            nodetree (_type_): _description_
            nodes (_type_): _description_
        """
        # update attribute
        # update nodes
        self.update_db_keys(
            self.db["node"],
            node["uuid"],
            {
                "name": node["name"],
                "label": node["label"],
                "action": node["action"],
                "inputs": node["inputs"],
                "outputs": node["outputs"],
                "properties": node["properties"],
                "position": node["position"],
            },
        )

    def updateNodetree(self):
        """Update a Nodetree

        Args:
            nodetree (_type_): _description_
            nodes (_type_): _description_
        """
        # update attribute
        # update nodes
        self.update_db_keys(
            self.db["nodetree"],
            self.nodetree["uuid"],
            {
                "name": self.nodetree["name"],
                "action": self.nodetree["action"],
                "nodes": self.nodetree["nodes"],
                "links": self.nodetree["links"],
            },
        )

    def update_db_keys(self, db, uuid, items={}):
        """update data and state to database"""
        query = {"uuid": uuid}
        newvalues = {"$set": items}
        db.update_one(query, newvalues)

    @staticmethod
    def getScinodeDB(editor):
        """get SciNode data from a Rete Editor data,
        save the nodetree and all nodes to db.

        Args:
            nodetree (dict): _description_
            nodes (dict): _description_
        """
        import pickle

        editor_nodes = editor.pop("nodes")
        nt_nodes = {}
        nodes = {}
        alllinks = []
        for key, ndata in editor_nodes.items():
            node = ndata.copy()
            # print("ndata: ", ndata)
            # editor.node.name => node.label
            # editor.node.id => node.name
            node["label"] = node["name"]
            node["name"] = str(node["id"])
            node["meta"]["nodetree_uuid"] = editor["uuid"]
            if node["meta"]["daemon_name"] == "":
                node["meta"]["daemon_name"] = editor["meta"]["daemon_name"]
            # fetch data for nodetree
            nt_nodes[key] = {
                "class_name": node["meta"]["class_name"],
                "name": node["id"],
                "uuid": node["uuid"],
                "node_type": node["meta"]["node_type"],
            }
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
            node["properties"] = pickle.dumps(node["properties"])
            node["results"] = pickle.dumps(tuple(node["results"]))
            node["outputs"] = node["outputs"]
            node["inputs"] = node["inputs"]
            # print('node: ', node)
            nodes[node["name"]] = node
            # insert_one(node, db['node'])
        # add links
        editor["links"] = []
        editor["nodes"] = nt_nodes
        # insert_one(editor, db['nodetree'])
        return editor, nodes
