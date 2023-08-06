editor.use(AutoArrangePlugin.default, { margin: {x: 50, y: 50 }, depth: 100 });
// load nodetree_data
console.log("input nodetree_data: ", nodetree_data)
editor
  .fromJSON(nodetree_data)
  .then(() => editor.trigger("process"))
  .then(loadNodetreeData(nodetree_data))
  .then(setStateColor());

// update node UI for selected nodes
editor.on("nodeselected", setSelectNodeUI);

editor.view.resize();
AreaPlugin.zoomAt(editor);
editor.trigger("process");

async function loadNodetreeData(nodetree_data) {
  await engine.abort();
  console.log("loadNodetreeData");
  editor.index = nodetree_data["index"];
  editor.name = nodetree_data["name"];
  editor.uuid = nodetree_data["uuid"];
  editor.state = nodetree_data["state"];
  editor.action = nodetree_data["action"];
  editor.meta.daemon_name = nodetree_data["meta"]["daemon_name"];
  // console.log("Editor: ", editor)
  setNode(nodetree_data);
  setNodetreeUI(nodetree_data);
}

function setNode(nodetree_data) {
  // set meta data to Node
  // uuid, nodetree_uuid
  console.log("nodes: ", editor.nodes.length);
  for (let i = 0; i < editor.nodes.length; i++) {
    // console.log(i, nodetree_data['nodes'][editor.nodes[i].id])
    editor.nodes[i].uuid = nodetree_data["nodes"][editor.nodes[i].id]["uuid"];
    // editor.nodes[i].counter = nodetree_data['nodes'][editor.nodes[i].id]['counter'];
    // console.log("set node state: ", i, nodetree_data["nodes"][editor.nodes[i].id]["state"])
    editor.nodes[i].name = nodetree_data["nodes"][editor.nodes[i].id]["label"];
    editor.nodes[i].state = nodetree_data["nodes"][editor.nodes[i].id]["state"];
    editor.nodes[i].meta.daemon_name =
      nodetree_data["nodes"][editor.nodes[i].id]["meta"]["daemon_name"];
    editor.nodes[i].update();
  }
}

function setNodetreeUI(nodetree_data) {
  // update html element based on data
  document.getElementById("nodetree_name").value = editor.name;
  document.getElementById("nodetree_daemon_name").value =
    editor.meta.daemon_name;
  document.getElementById("nodetree_uuid").value = editor.uuid;
  document.getElementById("nodetree_state").value = editor.state;
  document.getElementById("nodetree_action").value = editor.action;
}

function setNodetreeProps(data) {
  // set editor data by html element
  for (var key in data) {
    editor[key] = data[key];
  }
}

function setSelectedNodeProps(data) {
  // set editor data by html element
  var node = editor.selected.list[0];
  for (var key in data) {
    if (node.meta.hasOwnProperty(key)) {
      node.meta[key] = data[key];
    }
    else {
      node[key] = data[key];
    }
  }
  node.update();
}

async function nodetree_post(data, url) {
  // post nodetree data to app
  console.log("post Nodetree: ", data);
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Accept": "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  response.json().then((data) => {
    console.log(data);
    alert(data['message']);
    window.location.href = url + "/" + data["uuid"];
  });
}

async function nodetree_get(url) {
  // get nodetree data to app
  const response = await fetch(url)
    .then((response) => response.json())
    .then((data) => {
      var nodetree_data = data["nodetree_data"];
      // console.log("nodetree_get: ",nodetree_data);
      return nodetree_data;
    });
}

function saveNodetree() {
  // Launch nodetree
  editor.action = "NONE";
  var data = editor.toJSON();
  // post nodetree data
  nodetree_post(data, "/nodetrees");
}


function launchNodetree() {
  if (confirm("Are You Sure to launch this Nodetree?")) {
    // Launch nodetree
    editor.action = "LAUNCH";
    var data = editor.toJSON();
    // post nodetree data
    nodetree_post(data, "/nodetrees");
  }
}

function saveAsTemplate() {
  // Launch nodetree
  var data = editor.toJSON();
  // post nodetree data
  nodetree_post(data, "/templates");
}

function resetNodetree() {
  if (confirm("Are You Sure to reset this Nodetree?")) {
    // reset nodetree uuid
    editor.uuid = "";
    editor.name = "";
    // reset node too
    for (let i = 0; i < editor.nodes.length; i++) {
      editor.nodes[i].uuid = "";
      editor.nodes[i].counter = 0;
    }
    document.getElementById("nodetree_name").value = "";
    document.getElementById("nodetree_uuid").value = "";
  }
}

function setSelectNodeUI() {
  // update html element based on data
  if (editor.selected.list.length > 0) {
    document.getElementById("node_uuid").value = editor.selected.list[0].uuid;
    document.getElementById("node_name").value = editor.selected.list[0].name;
    document.getElementById("node_daemon_name").value =
      editor.selected.list[0].meta.daemon_name;
    document.getElementById("node_state").value = editor.selected.list[0].state;
  }
}

function actionSelectedNode(action) {
  // reset selected node
  if (confirm("Are You Sure to reset "+ editor.selected.list.length +" nodes?")) {
    var data = {};
    for (let i = 0; i < editor.selected.list.length; i++) {

      data[editor.selected.list[i].id] = action
    }
    nodetree_node_put(data);
    // editor.selected.list[i].state = "CREATED";
    // editor.selected.list[i].meta.daemon_name = "";
    // editor.selected.list[i].meta.counter = 0;
    // setSelectNodeUI();
  }
}


function actionNode(uuid, action) {
  // reset selected node
  for (let i = 0; i < editor.nodes.length; i++) {
    console.log(i, editor.nodes[i].uuid, uuid);
    if (editor.nodes[i].uuid == uuid) {
      console.log(i, action);
      editor.nodes[i].action = action;
      // put action
      node_put(editor.nodes[i].uuid, { action: action });
    }
  }
}

async function nodetree_node_put(data) {
  // put nodetree data to app
  console.log("put Nodetree node action: ", data);
  const response = await fetch("/nodetrees/"+ editor.uuid+"/nodes/action" , {
    method: "PUT",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  response.json().then((data) => {
    console.log(data);
  });
}

async function node_put(uuid, data) {
  // put nodetree data to app
  console.log("put Node: ", data);
  const response = await fetch("/nodes/" + uuid, {
    method: "PUT",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  response.json().then((data) => {
    console.log(data);
  });
}

function removeStateTag(item) {
  item.classList.remove("finished");
  item.classList.remove("failed");
  item.classList.remove("paused");
  item.classList.remove("running");
  item.classList.remove("waiting");
  item.classList.remove("created");
}

async function setStateColor() {
  await engine.abort();
  let s = document.getElementById("stateSwitchCheck");
  var titles = document.querySelectorAll(".node .title");
  if (s.checked) {
    for (let i = 0; i < editor.nodes.length; i++) {
      // remove old
      //   console.log("i: ", i)
      removeStateTag(titles[i]);
      titles[i].classList.add(editor.nodes[i].state.toLowerCase());
    }
  } else {
    for (let i = 0; i < editor.nodes.length; i++) {
      removeStateTag(titles[i]);
    }
  }
}

async function refreshNodetree() {
  // reload nodetree
  if (editor.uuid != "") {
    const response = await fetch("/nodetrees/api/" + editor.uuid)
      .then((response) => response.json())
      .then((data) => {
        var nodetree_data = data["nodetree_data"];
        // console.log("nodetree_data: ", nodetree_data);
        editor
          .fromJSON(nodetree_data)
          .then(() => editor.trigger("process"))
          .then(loadNodetreeData(nodetree_data))
          .then(setStateColor());
      });
  }
}

function arrangeNodetree() {
  console.log('Arranging...')
  editor.trigger('arrange');
}
