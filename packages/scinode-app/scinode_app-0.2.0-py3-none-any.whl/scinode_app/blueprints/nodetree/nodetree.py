from flask import Blueprint, render_template, request
from scinode_app.db import db

nodetree_bp = Blueprint("nodetree_bp", __name__, template_folder="templates")


# =================================
# NodeTree
# =================================


@nodetree_bp.route("/")
def nodetrees():
    """Nodetree table
    This is a page to show the table.
    The actual data is read from /api/nodetree_table using GET method.
    """
    return render_template("nodetree_table.html", title="Nodetree Table")


@nodetree_bp.route("/<uuid>")
def nodetree_get(uuid):
    """Show nodetree with this uuid

    Args:
        uuid (str): uuid the nodetree to be shown
    """
    from scinode_app.utils.rete_adapter import ReteAdaptor

    query = {"uuid": uuid}
    nodetree_data = ReteAdaptor.getEditor(query, db)
    # print("getEditor, nodetree_data: ", nodetree_data)
    return render_template(
        "nodetree_editor.html", title="Nodetree", nodetree_data=nodetree_data
    )


@nodetree_bp.route("/", methods=["POST"])
def nodetree_post():
    """Creat a new nodetree

    Returns:
        dict: uuid of the created nodetree, which will be used
        to redirect the page to show this nodetree.
    """
    from scinode_app.utils.rete_adapter import ReteAdaptor
    from scinode.engine.nodetree_launch import LaunchNodeTree

    editor = request.json
    ntdata = ReteAdaptor.getScinodeDB(editor)
    print("post: ", ntdata)
    lnt = LaunchNodeTree(ntdata)
    if ntdata["action"] == "LAUNCH":
        lnt.launch()
        return {
            "uuid": ntdata["uuid"],
            "message": "Launch Nodetree: {} successfully".format(ntdata["name"]),
        }
    else:
        lnt.save()
        return {
            "uuid": ntdata["uuid"],
            "message": "Save Nodetree: {} successfully".format(ntdata["name"]),
        }


@nodetree_bp.route("/<uuid>", methods=["PUT"])
def nodetree_put(uuid):
    """Update nodetree data

    Args:
        uuid (str): uuid of the nodetree to be updated
    """
    content_type = request.headers.get("Content-Type")
    json = request.json
    query = {"name": uuid}
    query = db["nodetree"].find(query, {"_id": 0})
    return {"message": True}


@nodetree_bp.route("/<uuid>/nodes/action", methods=["PUT"])
def nodetree_node_action_put(uuid):
    """Apply actions to the nodes of this nodetree.

    The request.json should be a dict which includes the name
    and action for each node.

    Args:
        uuid (str): uuid of the nodetree

    Returns:
        dict: message
    """
    from scinode.engine.nodetree_engine import EngineNodeTree

    content_type = request.headers.get("Content-Type")
    data = request.json
    nt = EngineNodeTree(uuid=uuid)
    for name, action in data.items():
        if action == "RESET":
            nt.reset_node(name=name)
        elif action == "PAUSE":
            nt.pause_node(name=name)
        elif action == "PLAY":
            nt.play_node(name=name)
    return {"message": True}


@nodetree_bp.route("/<uuid>", methods=["DELETE"])
def nodetree_delete(uuid):
    """Delete a nodetree.

    This will delete the nodetree in the database.

    Args:
        uuid (str): uuid of nodetree to be deleted.

    Returns:
        dict: message
    """
    from scinode.database.db import ScinodeDB

    db = ScinodeDB()
    query = {}
    query["uuid"] = uuid
    db.delete_nodetree(query)
    return {"message": "Delete nodetree: {} successfully!".format(uuid)}


@nodetree_bp.route("/api/<uuid>")
def api_nodetree_get(uuid):
    """Get nodetree data from database.

    Args:
        uuid (str): uuid of the nodetree

    Returns:
        dict: nodetree_data
    """
    from scinode_app.utils.rete_adapter import ReteAdaptor

    query = {"uuid": uuid}
    nodetree_data = ReteAdaptor.getEditor(query, db)
    # print(nodetree_data)
    return {
        "nodetree_data": nodetree_data,
    }


@nodetree_bp.route("/api/nodetree_data")
def nodetree_data():
    """Query the nodetree data from database.

    1) Qeury based on platform and search text
    2) Sort the data
    3) Pagination the data

    Returns:
        dict: nodetree_data, recordsFiltered, recordsTotal
    """
    from scinode_app.db import query_nodetree_data

    query = {}
    query, total_filtered, recordsTotal = query_nodetree_data(
        db["nodetree"], query, request
    )
    # nodetree_data
    nodetree_data = list(query)
    for data in nodetree_data:
        # print(data)
        data["daemon_name"] = data["meta"]["daemon_name"]
    # response
    return {
        "data": nodetree_data,
        "recordsFiltered": total_filtered,
        "recordsTotal": recordsTotal,
        "draw": request.args.get("draw", type=int),
    }


@nodetree_bp.route("/api/<uuid>/nodes")
def nodetree_nodes(uuid):
    """_summary_

    Args:
        uuid (_type_): _description_

    Returns:
        _type_: _description_
    """
    from scinode_app.db import query_node_data

    query = {"meta.nodetree_uuid": uuid}
    query, total_filtered, recordsTotal = query_node_data(db["node"], query, request)
    # node_data
    node_data = list(query)
    # print(node_data)
    for d in node_data:
        d["name"] = d["meta"]["class_name"]
    # response
    return {
        "data": node_data,
        "recordsFiltered": total_filtered,
        "recordsTotal": recordsTotal,
        "draw": request.args.get("draw", type=int),
    }


@nodetree_bp.route("/importer")
def nodetree_importer():
    return render_template("nodetree_importer.html")


@nodetree_bp.route("importer", methods=["POST"])
def nodetree_importer_api():
    from scinode_app.build_node_from_json import build_components_from_db
    from flask import flash, redirect
    import json
    import uuid

    # check if the post request has the file part
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)
    file = request.files["file"]
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == "":
        flash("No selected file")
        return redirect(request.url)
    data = json.loads(file.read())
    n = len(data)
    # check name
    # check uuid and name
    for item in data:
        if "uuid" not in item or item["uuid"] == "":
            item["uuid"] = str(uuid.uuid4())
    #
    db["component"].insert_many(data)
    build_components_from_db()
    return {
        "success": True,
        "message": "Import {} components successfully!".format(n),
    }


@nodetree_bp.route("/exporter")
def nodetrees_exporter():
    return render_template("nodetree_exporter.html")


@nodetree_bp.route("/download-json", methods=["GET"])
def nodetree_download_json():
    from flask import Response
    from bson.json_util import dumps

    nodetrees = db["nodetree"].find({}, {"_id": 0})
    nodetrees = dumps(list(nodetrees), indent=2)
    return Response(
        nodetrees,
        mimetype="application/json",
        headers={"Content-Disposition": "attachment;filename=nodetrees.json"},
    )


@nodetree_bp.route("/download-python/<uuid>/", methods=["GET"])
def nodetree_download_python(uuid):
    from flask import Response
    from bson.json_util import dumps
    from .utils import build_nodetree_python_script

    nodetree = db["nodetree"].find_one({"uuid": uuid}, {"_id": 0})
    # fetch nodes
    nodes = db["node"].find({"meta.nodetree_uuid": uuid}, {"_id": 0, "results": 0})
    script = build_nodetree_python_script(nodetree, nodes)
    print(script)
    return Response(
        script,
        mimetype="application/json",
        headers={"Content-Disposition": "attachment;filename=nodetrees.py"},
    )
