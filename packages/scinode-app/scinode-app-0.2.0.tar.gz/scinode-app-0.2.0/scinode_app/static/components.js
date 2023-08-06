

class ScinodeScatterComponent extends ScinodeComponent {

    constructor(){
        super("ScinodeScatter");
        this.catalog = 'Control';
        this.name = "ScinodeScatter";
        this.node_type = 'Scatter';

    }

    builder(node) {
        this.init(node);
        node.meta.kwargs = ['Input', 'Stop'];
        node.executor = {"path": "scinode.executors.controls.scatter_node",
          "name": "ScinodeScatter",
          "type": "class",
          };
        var inp1 = new Rete.Input('Input',"Input", SocketGeneral, true);
        var inp2 = new Rete.Input('Stop',"Stop", SocketGeneral);
        var out1 = new Rete.Output('Result', "Result", SocketGeneral);
        node.addInput(inp1);
        node.addInput(inp2);
        node.addOutput(out1);
        return node
    }
}

class ScinodeSwitchComponent extends ScinodeComponent {

    constructor(){
        super("ScinodeSwitch");
        this.catalog = 'Control';
        this.name = "ScinodeSwitch";
        this.node_type = 'Switch';
    }

    builder(node) {
        this.init(node);
        node.meta.kwargs = ['Input', 'Switch'];
        node.executor = {"path": "scinode.executors.controls.switch_node",
          "name": "ScinodeSwitch",
          "type": "class",
          };
        var inp1 = new Rete.Input('Input',"Input", SocketGeneral);
        var inp2 = new Rete.Input('Switch',"Switch", SocketGeneral);
        var out1 = new Rete.Output('Result', "Result", SocketGeneral);
        node.addInput(inp1);
        node.addInput(inp2);
        node.addOutput(out1);
        return node
    }
}


class ScinodeUpdateComponent extends ScinodeComponent {

    constructor(){
        super("ScinodeUpdate");
        this.catalog = 'Control';
        this.name = "ScinodeUpdate";
        this.node_type = 'Update';
    }

    builder(node) {
        this.init(node);
        node.meta.kwargs = ['Input', 'Update'];
        node.executor = {"path": "scinode.executors.controls.update_node",
          "name": "ScinodeUpdate",
          "type": "class",
          };
        var inp1 = new Rete.Input('Input',"Input", SocketGeneral);
        var inp2 = new Rete.Input('Update',"Update", SocketGeneral);
        var out1 = new Rete.Output('Result', "Result", SocketGeneral);
        node.addInput(inp1);
        node.addInput(inp2);
        node.addOutput(out1);
        return node
    }
}


class StringComponent extends ScinodeComponent {

    constructor(){
        super("String");
        this.catalog = 'Test';
        this.name = "string"
    }

    builder(node) {
        this.init(node);
        node.meta.kwargs = ['str'];
        node.executor = {"path": "scinode.executors.built_in",
          "name": "PropertyToSocket",
          "type": "class",
          };
        var out1 = new Rete.Output('str', "str", SocketString);

        node.addControl(new StringControl(this.editor, 'str'));
        node.addOutput(out1);
        return node
    }
}
class TestFloatComponent extends ScinodeComponent {

    constructor(){
        super("TestFloat");
        this.catalog = 'Test';
        this.name = "TestFloat";
    }

    builder(node) {
        this.init(node);
        node.meta.args = [];
        node.meta.kwargs = ['Float'];
        node.executor = {"path": "scinode.executors.built_in",
          "name": "PropertyToSocket",
          "type": "class",
          };
        var out1 = new Rete.Output('Float', "Float", SocketFloat);

        node.addControl(new FloatControl(this.editor, 'Float'));
        node.addOutput(out1);
        return node
    }
}


class TestDelayAddComponent extends ScinodeComponent {
    constructor(){
        super("TestDelayAdd");
        this.catalog = 'Test';
        this.name = 'TestDelayAdd'
    }

    builder(node) {
        this.init(node)
        node.meta.kwargs = ['t', 'x', 'y'];
        node.executor = {"path": "scinode.executors.test.math",
                        "name": 'add',
                        };

        var ctl1 = new FloatControl(this.editor, 't');
        var inp1 = new Rete.Input('x',"x", SocketFloat);
        var inp2 = new Rete.Input('y', "y", SocketFloat);
        var out = new Rete.Output('Result', "Result", SocketFloat);

        inp1.addControl(new FloatControl(this.editor, 'x'))
        inp2.addControl(new FloatControl(this.editor, 'y'))

        node.addControl(ctl1)
            .addInput(inp1)
            .addInput(inp2)
            .addOutput(out);
        return node
    }
}



class TestDelayMinusComponent extends ScinodeComponent {
    constructor(){
        super("TestDelayMinus");
        this.catalog = 'Test';
        this.name = 'TestDelayMinus'
    }

    builder(node) {
        this.init(node)
        node.meta.kwargs = ['t', 'x', 'y'];
        node.executor = {"path": "scinode.executors.test.math",
                        "name": 'minus',
                        };

        var ctl1 = new FloatControl(this.editor, 't');
        var inp1 = new Rete.Input('x',"x", SocketFloat);
        var inp2 = new Rete.Input('y', "y", SocketFloat);
        var out = new Rete.Output('Result', "Result", SocketFloat);

        inp1.addControl(new FloatControl(this.editor, 'x'))
        inp2.addControl(new FloatControl(this.editor, 'y'))

        node.addControl(ctl1)
            .addInput(inp1)
            .addInput(inp2)
            .addOutput(out);
        return node
    }
}

class TestDelayGreaterComponent extends ScinodeComponent {
    constructor(){
        super("TestDelayGreater");
        this.catalog = 'Test';
        this.name = 'TestDelayGreater'
    }

    builder(node) {
        this.init(node)
        node.meta.kwargs = ['t', 'x', 'y'];
        node.executor = {"path": "scinode.executors.test.math",
                        "name": 'greater',
                        };

        var ctl1 = new FloatControl(this.editor, 't');
        var inp1 = new Rete.Input('x',"x", SocketFloat);
        var inp2 = new Rete.Input('y', "y", SocketFloat);
        var out = new Rete.Output('Result', "Result", SocketFloat);

        inp1.addControl(new FloatControl(this.editor, 'x'))
        inp2.addControl(new FloatControl(this.editor, 'y'))

        node.addControl(ctl1)
            .addInput(inp1)
            .addInput(inp2)
            .addOutput(out);
        return node
    }
}


class TestDelayLessComponent extends ScinodeComponent {
    constructor(){
        super("TestDelayLess");
        this.catalog = 'Test';
        this.name = 'TestDelayLess'
    }

    builder(node) {
        this.init(node)
        node.meta.kwargs = ['t', 'x', 'y'];
        node.executor = {"path": "scinode.executors.test.math",
                        "name": 'less',
                        };

        var ctl1 = new FloatControl(this.editor, 't');
        var inp1 = new Rete.Input('x',"x", SocketFloat);
        var inp2 = new Rete.Input('y', "y", SocketFloat);
        var out = new Rete.Output('Result', "Result", SocketFloat);

        inp1.addControl(new FloatControl(this.editor, 'x'))
        inp2.addControl(new FloatControl(this.editor, 'y'))

        node.addControl(ctl1)
            .addInput(inp1)
            .addInput(inp2)
            .addOutput(out);
        return node
    }
}


class TestRangeComponent extends ScinodeComponent {
    constructor(){
        super("TestRange");
        this.catalog = 'Test';
        this.name = 'TestRange'
    }

    builder(node) {
        this.init(node)
        node.meta.kwargs = ["start", "stop", "step"]
        node.executor = {"path": "scinode.executors.test.math",
                        "name": 'test_range',
                        };

        var ctl1 = new FloatControl(this.editor, 'start');
        var ctl2 = new FloatControl(this.editor, 'stop');
        var ctl3 = new FloatControl(this.editor, 'step');
        var out = new Rete.Output('Result', "Result", SocketFloat);

        node.addControl(ctl1)
            .addControl(ctl2)
            .addControl(ctl3)
            .addOutput(out);
        return node
    }
}

var components = [
    new ScinodeScatterComponent(),
    new ScinodeSwitchComponent(),
    new ScinodeUpdateComponent(),
    new StringComponent(),
    new TestFloatComponent(),
    new TestDelayAddComponent(),
    new TestDelayMinusComponent(),
    new TestDelayGreaterComponent(),
    new TestDelayLessComponent(),
    new TestRangeComponent(),
];
