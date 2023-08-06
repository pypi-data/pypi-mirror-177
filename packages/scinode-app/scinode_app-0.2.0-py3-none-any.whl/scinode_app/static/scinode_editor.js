class ScinodeEditor extends Rete.NodeEditor {

    constructor(id, container){
        super(id, container);
        this.name = 'NodeTree'
        this.meta = {"daemon_name": 'localhost',
                    "parent": "",
                    "platform": "rete",
                    "scatter_node": "",
                };
        this.uuid = ''
        this.state = ''
        this.action = ''
    }

    // override the toJSON method
    toJSON() {
        var data = super.toJSON()
        data['name'] = editor.name;
        data['uuid'] = editor.uuid;
        data['state'] = editor.state;
        data['action'] = editor.action;
        data['meta'] = editor.meta,
        data['links'] = [];
        data['description'] = "";
        data['log'] = "";
        return data;
    }
}
