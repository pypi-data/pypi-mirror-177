scinode_controls = {
    "Float": "FloatControl",
    "String": "StringControl",
    "Bool": "BoolControl",
    "FloatVector": "FloatVectorControl",
    "FloatMatrix": "FloatMatrixControl",
    "Color": "ColorControl",
    "File": "FileControl",
    "Enum": "EnumControl",
    "PlotlyBasicChart": "PlotlyBasicChartControl",
}


template = [
    {
        "name": "Test",
        "meta": {
            "catalog": "Template",
            "args": ["x", "y"],
            "kwargs": [],
        },
        "executor": {
            "path": "numpy",
            "name": "add",
            "type": "function",
        },
        "controls": [
            {
                "name": "text",
                "type": "String",
                "defaultVal": "abc",
            },
            {
                "name": "float",
                "type": "Float",
                "defaultVal": 10.0,
            },
            {
                "name": "enum",
                "type": "Enum",
                "defaultVal": 0,
                "options": ["a", "b", "c"],
            },
            {
                "name": "bool",
                "type": "Bool",
                "defaultVal": True,
            },
            {
                "name": "matrix",
                "type": "FloatMatrix",
                "size": [2, 3],
                "defaultVal": [1, 2, 3, 4, 5, 6],
            },
        ],
        "inputs": [
            {
                "name": "input1",
                "type": "SocketFloat",
                "control": {
                    "type": "Float",
                    "defaultVal": 0,
                },
            },
            {
                "name": "input2",
                "type": "SocketFloatVector",
                "control": {
                    "type": "FloatVector",
                    "size": 3,
                    "defaultVal": [1, 2, 3],
                },
            },
        ],
        "outputs": [
            {
                "name": "Output",
                "type": "SocketFloat",
            },
        ],
    }
]


class ComponentFromString:
    def __init__(self, ndata) -> None:

        self.ndata = ndata

    def build_component_string(self):
        """Build component string"""
        header_string = self.build_header()
        init_string = self.build_sockets()
        control_string = self.build_controls()
        executor_string = self.build_executor()
        # print(header_string)
        # print(control_string)
        # print(init_string)
        # print(executor_string)
        code = header_string + control_string + init_string + executor_string
        code += """
        return node
    }
}"""
        return code

    def build_header(self):
        """Build header of the component."""
        ndata = self.ndata
        header_string = """
class {0}{1}Component extends ScinodeComponent {{

    constructor(){{
        super("{0}{1}");
        this.catalog = "{0}";
        this.name = "{1}";
    }}

    builder(node) {{
        this.init(node);
        node.meta.args = {2};
        node.meta.kwargs = {3};
    """.format(
            ndata["meta"]["catalog"],
            ndata["name"],
            ndata["meta"]["args"],
            ndata["meta"]["kwargs"],
        )
        return header_string

    def build_controls(self):
        """Build Controls
        the python data is converted to json data.
        """
        import json

        if "controls" not in self.ndata:
            return ""
        s = ""
        for data in self.ndata["controls"]:
            print(data)
            # print(json.dumps(data))
            s += """
        node.addControl(new {0}(this.editor, "{1}", {2}));""".format(
                scinode_controls[data["type"]], data["name"], json.dumps(data)
            )
        return s

    def build_sockets(self):
        """Build input and output sockets."""
        inputs = self.ndata["inputs"]
        init_string = """"""
        n = len(inputs)
        for i in range(n):
            init_string += self.build_socket(i, inputs[i], "Input")
        outputs = self.ndata["outputs"]
        n = len(outputs)
        for i in range(n):
            init_string += self.build_socket(i, outputs[i], "Output")
        return init_string

    def build_socket(self, i, data, collection):
        """Build single socket."""
        import json

        var = "inp{}".format(i) if collection == "Input" else "out{}".format(i)
        s = """
        var {0} = new Rete.{1}("{2}","{2}", {3});""".format(
            var, collection, data["name"], data["type"]
        )
        if "control" in data and data["control"]["type"] != "None":
            s += """
        {0}.addControl(new {1}(this.editor, "{2}", {3}));""".format(
                var,
                scinode_controls[data["control"]["type"]],
                data["name"],
                json.dumps(data["control"]),
            )
        # mount to node
        s += """
        node.add{0}({1});""".format(
            collection, var
        )

        return s

    def build_executor(self):
        import json

        s = """
        node.executor = {};
    """.format(
            json.dumps(self.ndata["executor"])
        )
        return s


def build_components_to_js(data):
    """Build components into a javascript code.

    Args:
        data (dict): json data of the components.

    Returns:
        string: text of the components
    """
    c = ComponentFromString(data)
    s = ""
    components = "\nvar json_components = ["
    for ndata in data:
        c.ndata = ndata
        s += c.build_component_string()
        components += "new {}{}Component(), \n".format(
            ndata["meta"]["catalog"], ndata["name"]
        )
    components += "];"
    s += components
    return s


def save_components_to_js(s):
    """Save components to javascript file

    Args:
        s (string): text of the components
    """
    import pathlib
    import os

    path = pathlib.Path(__file__).parent.resolve()
    with open(os.path.join(path, "static/json_components.js"), "w") as f:
        f.write(s)


def build_components_from_db():
    """Build compnents from database"""
    from scinode.database.db import scinodedb

    data = list(scinodedb["component"].find({}))
    s = build_components_to_js(data)
    save_components_to_js(s)


if __name__ == "__main__":
    from scinode.database.db import scinodedb

    data = list(scinodedb["component"].find({}))
    s = build_components_to_js(data)
    save_components_to_js(s)
