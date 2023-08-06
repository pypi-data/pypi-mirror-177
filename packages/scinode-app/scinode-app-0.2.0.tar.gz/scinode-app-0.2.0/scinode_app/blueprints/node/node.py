from flask import Blueprint, render_template, request
from scinode_app.db import db

node_bp = Blueprint("node_bp", __name__, template_folder="templates")


@node_bp.route("/")
def nodes():
    return render_template("node_table.html", title="Node Table")


@node_bp.route("/api/node_data")
def node_data():
    from scinode_app.db import query_node_data

    query = {}
    query, total_filtered, recordsTotal = query_node_data(db["node"], query, request)
    # node_data
    node_data = []
    for record in query:
        data = {}
        data["index"] = record["index"]
        data["uuid"] = record["uuid"]
        data["name"] = record["meta"]["class_name"]
        data["state"] = record["state"]
        data["action"] = record["action"]
        node_data.append(data)
    # print("node_data:", node_data)
    # response
    return {
        "data": node_data,
        "recordsFiltered": total_filtered,
        "recordsTotal": recordsTotal,
        "draw": request.args.get("draw", type=int),
    }


@node_bp.route("/<uuid>")
def node_get(uuid):
    """Get node data

    Args:
        uuid (str): uuid of the node

    Returns:
        _type_: _description_
    """
    import pickle

    query = {"uuid": uuid}
    query = db["node"].find(query, {"_id": 0})
    # node_data
    node_data = list(query)[0]
    # print(node_data)
    node_data["properties"] = pickle.loads(node_data["properties"])
    node_data["results"] = pickle.loads(node_data["results"])
    # change to string for display
    node_data["properties"] = node_data["properties"]
    for key, p in node_data["properties"].items():
        p["value"] = str(p["value"])
    node_data["results"] = node_data["results"]
    for data in node_data["results"]:
        data["value"] = str(data["value"])
    # print(node_data)
    return render_template("node_viewer.html", title="Node", node_data=node_data)


# put: put a nodetree
@node_bp.route("/<uuid>", methods=["PUT"])
def node_put(uuid):
    items = request.json
    query = {"uuid": uuid}
    newvalues = {"$set": items}
    db["node"].update_one(query, newvalues)
    return {"message": True}


# delete: delete a node
@node_bp.route("/<uuid>", methods=["DELETE"])
def node_delete(uuid):
    query = {"uuid": uuid}
    print(query)
    db["node"].delete_one(query)
    return {"message": "Delete nodet: {} successfully!".format(uuid)}
