from flask import Blueprint, render_template, request
from scinode_app.db import db

config_bp = Blueprint("config_bp", __name__, template_folder="templates")


# =================================
# componetns
# =================================
@config_bp.route("/")
def configs():
    return render_template("config.html", title="Configuration")


@config_bp.route("/daemons/logfile/<name>")
def daemon_logfile(name):
    from scinode.daemon.daemon import ScinodeDaemon

    daemon = ScinodeDaemon(name=name)
    with open(daemon.logfile) as f:
        log_data = f.readlines()
    return render_template("daemon_logfile.html", title="Logfile", log_data=log_data)


@config_bp.route("/api/daemon_data")
def daemon_data():
    from scinode.daemon.daemon import ScinodeDaemon
    from scinode.config import DaemonConfig
    import pandas as pd

    config = DaemonConfig()
    daemon_datas = config.datas
    status = []
    for data in daemon_datas:
        daemon = ScinodeDaemon(name=data["name"])
        pid, is_running = daemon.get_status()
        if is_running == 0:
            status.append(
                {
                    "name": data["name"],
                    "workdir": data["workdir"],
                    "pid": int(pid),
                    "status": "Running",
                }
            )
        else:
            status.append(
                {
                    "name": data["name"],
                    "workdir": data["workdir"],
                    "pid": "",
                    "status": "Not running",
                }
            )
    print("daemon_data:", status)
    # response
    return {
        "data": status,
        "recordsFiltered": 0,
        "recordsTotal": 0,
        "draw": request.args.get("draw", type=int),
    }


@config_bp.route("/api/daemon_add", methods=["POST"])
def daemon_add():
    from scinode.config import DaemonConfig

    json = request.json
    config = DaemonConfig()
    print("daemon: ", json)
    if json["name"] == "":
        return {"message": "Name is empty. Please input a value"}
    elif json["workdir"] == "":
        return {"message": "Work directory is empty. Please input a value"}
    else:
        config.insert_one(json)
    return {"message": "Add daemon {} successfully".format(json["name"])}


@config_bp.route("/api/daemon_action", methods=["POST"])
def daemon_action():
    from scinode.config import DaemonConfig
    from scinode.daemon.daemon import ScinodeDaemon
    import os

    json = request.json
    print("daemon action: ", json)
    config = DaemonConfig()
    query = {}
    name = json.get("name")
    action = json.get("action")
    if name:
        query["name"] = name
    if action.upper() == "DELETE":
        os.system("scinode daemon delete --name {}".format(name))
        # config.delete(query)
        return {"message": "Delete {} successfully".format(name)}
    elif action.upper() == "STOP":
        daemon = ScinodeDaemon(name)
        print("Stop")
        # daemon.stop()
        os.system("scinode daemon stop {}".format(name))
        return {"message": "Stop {} successfully".format(name)}
    elif action.upper() == "START":
        daemon = ScinodeDaemon(name)
        os.system("scinode daemon start {}".format(name))
        # daemon.start()
        return {"message": "Start {} successfully".format(name)}
    elif action.upper() == "RESTART":
        daemon = ScinodeDaemon(name)
        os.system("scinode daemon restart {}".format(name))
        # daemon.restart()
        return {"message": "Restart {} successfully".format(name)}
    # response
    return {"message": "None"}
