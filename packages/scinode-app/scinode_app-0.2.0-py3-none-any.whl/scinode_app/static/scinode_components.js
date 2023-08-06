
class ScinodeComponent extends Rete.Component {

    constructor(name){
        super(name);
    }

    init(node) {
        node.uuid = '';
        node.state = 'CREATED',
        node.action = 'NONE',
        node.setMeta({
        "class_name": this.name,
        "nodetree_uuid": '',
        "daemon_name": '',
        "counter": 0,
        "catalog": this.catalog,
        "node_type": this.node_type === undefined ? "Normal": this.node_type,
        "scattered_from": '',
        "scattered_label": '',
        "args": [],
        "kwargs": [],
        "platform": 'rete',
        });
        node.executor = {"path": "scinode.executors.built_in",
          "name": "PropertyToSocket",
          "type": "class",
          };
        // override the toJSON method
        node.builtin_toJSON = node.toJSON
        node.toJSON = function toJSON() {
            var data = this.builtin_toJSON();
            data['uuid'] = this.uuid;
            data['state'] = this.state;
            data['action'] = this.action;
            data['meta'] = this.meta;
            data['executor'] = this.executor;
            data['results'] = [];
            data['controls'] = {};
            data['description'] = "";
            data['log'] = "";
            this.controls.forEach(function(control, key) {
                data['controls'][key] = {'name': control.key, 'data': control.data, 'type': control.type}
            })
            this.inputs.forEach(function(input, key) {
                let control = input.control;
                if (control != undefined) {
                    data['controls'][key] = {'name': control.key, 'data': control.data, 'type': control.type}
                }
            })
            // output results
            this.outputs.forEach(function(value, key) {
                data['results'].push({'name': value.key, 'value': 0});
            })
            return data;
        }
    }
    builder(node) {
        this.init(node);
        return node
    }
}


class TemplateComponent extends ScinodeComponent {

    constructor(){
        super("Template");
        this.name = "Template";
        this.catalog = 'Template';
    }

    builder(node) {
        this.init(node);
        node.executor = {"path": "scinode.executors.built_in",
          "name": "PropertyToSocket",
          "type": "class",
          };
        var inp1 = new Rete.Input('input1', "input1", SocketFloat);
        var inp2 = new Rete.Input('input2', "input2", SocketFloat);
        var out1 = new Rete.Output('output', "output", SocketFloat);

        node.addControl(new FloatControl(this.editor, 'control1'));
        node.addControl(new StringControl(this.editor, 'control2'));
        inp1.addControl(new FloatControl(this.editor, 'input1'));
        node.addInput(inp1);
        node.addInput(inp2);
        node.addOutput(out1);
        node.kwargs = ['input'];
        return node
    }
}
