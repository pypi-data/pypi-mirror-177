from flask import Flask, render_template, request
from scinode_app.db import db
from scinode_app.blueprints.node.node import node_bp
from scinode_app.blueprints.component.component import component_bp
from scinode_app.blueprints.nodetree.nodetree import nodetree_bp
from scinode_app.blueprints.template.template import template_bp
from scinode_app.blueprints.config.config import config_bp

app = Flask(__name__)

app.register_blueprint(node_bp, url_prefix="/nodes")
app.register_blueprint(component_bp, url_prefix="/components")
app.register_blueprint(nodetree_bp, url_prefix="/nodetrees")
app.register_blueprint(template_bp, url_prefix="/templates")
app.register_blueprint(config_bp, url_prefix="/configs")

# =================================
# Home page
# =================================


@app.route("/")
def index():
    """Home page
    1) Show button for nodetree and template
    2) Show statistic data of the database.
    """
    nodetreeTotal = db["nodetree"].count_documents({})
    nodeTotal = db["node"].count_documents({})
    componentTotal = db["component"].count_documents({})
    templateTotal = db["template_nodetree"].count_documents({})
    return render_template(
        "index.html",
        title="",
        nodetreeTotal=nodetreeTotal,
        nodeTotal=nodeTotal,
        componentTotal=componentTotal,
        templateTotal=templateTotal,
    )


@app.route("/nodetree_editor")
def nodetree_editor():
    """Nodetree editor.

    Initialize a editor without node.
    """
    from scinode_app.init_data import init_nodetree_data

    return render_template(
        "nodetree_editor.html", title="Nodetree", nodetree_data=init_nodetree_data
    )


# ====================================
# Others
# ====================================


@app.route("/api/file_upload", methods=["POST"])
def file_upload_api():
    from flask import flash, redirect
    import json

    # check if the post request has the file part
    print(request.files)
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
    print("data: ", data)
    return {
        "success": True,
        "content": data,
    }


if __name__ == "__main__":
    app.run()
