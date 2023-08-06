
class TemplateTestComponent extends ScinodeComponent {

    constructor(){
        super("TemplateTest");
        this.catalog = "Template";
        this.name = "Test";
    }

    builder(node) {
        this.init(node);
        node.meta.args = ['x', 'y'];
        node.meta.kwargs = [];
    
        node.addControl(new StringControl(this.editor, "text", {"name": "text", "type": "String", "defaultVal": "abc"}));
        node.addControl(new FloatControl(this.editor, "float", {"name": "float", "type": "Float", "defaultVal": 10}));
        node.addControl(new EnumControl(this.editor, "enum", {"name": "enum", "type": "Enum", "defaultVal": 0, "options": ["a", "b", "c"]}));
        node.addControl(new BoolControl(this.editor, "bool", {"name": "bool", "type": "Bool", "defaultVal": true}));
        var inp0 = new Rete.Input("input1","input1", SocketFloat);
        inp0.addControl(new FloatControl(this.editor, "input1", {"defaultVal": 0, "type": "Float"}));
        node.addInput(inp0);
        var inp1 = new Rete.Input("input2","input2", SocketFloatVector);
        inp1.addControl(new FloatVectorControl(this.editor, "input2", {"defaultVal": [1, 2, 3], "size": 3, "type": "FloatVector"}));
        node.addInput(inp1);
        var out0 = new Rete.Output("Output","Output", SocketFloat);
        node.addOutput(out0);
        node.executor = {"path": "numpy", "name": "add", "type": "function"};
    
        return node
    }
}
class QEPWParameterComponent extends ScinodeComponent {

    constructor(){
        super("QEPWParameter");
        this.catalog = "QE";
        this.name = "PWParameter";
    }

    builder(node) {
        this.init(node);
        node.meta.args = [];
        node.meta.kwargs = ['calculation', 'ecutwfc', 'occupations', 'smearing', 'degauss', 'nspin'];
    
        node.addControl(new EnumControl(this.editor, "calculation", {"name": "calculation", "type": "Enum", "defaultVal": "scf", "options": ["scf", "relax", "nscf", "bands", "relax", "md", "vc-relax", "vc-md"]}));
        node.addControl(new FloatControl(this.editor, "ecutwfc", {"name": "ecutwfc", "type": "Float", "defaultVal": 30}));
        node.addControl(new StringControl(this.editor, "occupations", {"name": "occupations", "type": "String", "defaultVal": "smearing"}));
        node.addControl(new StringControl(this.editor, "smearing", {"name": "smearing", "type": "String", "defaultVal": "gaussian"}));
        node.addControl(new FloatControl(this.editor, "degauss", {"name": "degauss", "type": "Float", "defaultVal": 0.02}));
        node.addControl(new FloatControl(this.editor, "nspin", {"name": "nspin", "type": "Float", "defaultVal": 1}));
        var out0 = new Rete.Output("Parameter","Parameter", SocketGeneral);
        node.addOutput(out0);
        node.executor = {"path": "scinode.executors.built_in", "name": "PropertyToSocket", "type": "class"};
    
        return node
    }
}
class QEDosParameterComponent extends ScinodeComponent {

    constructor(){
        super("QEDosParameter");
        this.catalog = "QE";
        this.name = "DosParameter";
    }

    builder(node) {
        this.init(node);
        node.meta.args = [];
        node.meta.kwargs = ['deguass', 'Emin', 'Emax', 'DeltaE'];
    
        node.addControl(new FloatControl(this.editor, "deguass", {"name": "deguass", "type": "Float", "defaultVal": 0.01}));
        node.addControl(new FloatControl(this.editor, "Emin", {"name": "Emin", "type": "Float", "defaultVal": -10}));
        node.addControl(new FloatControl(this.editor, "Emax", {"name": "Emax", "type": "Float", "defaultVal": 10}));
        node.addControl(new FloatControl(this.editor, "DeltaE", {"name": "DeltaE", "type": "Float", "defaultVal": 0.02}));
        var out0 = new Rete.Output("Parameter","Parameter", SocketGeneral);
        node.addOutput(out0);
        node.executor = {"path": "scinode.executors.built_in", "name": "PropertyToSocket", "type": "class"};
    
        return node
    }
}
class QEProjwfcParameterComponent extends ScinodeComponent {

    constructor(){
        super("QEProjwfcParameter");
        this.catalog = "QE";
        this.name = "ProjwfcParameter";
    }

    builder(node) {
        this.init(node);
        node.meta.args = [];
        node.meta.kwargs = ['deguass', 'Emin', 'Emax', 'DeltaE'];
    
        node.addControl(new FloatControl(this.editor, "deguass", {"name": "deguass", "type": "Float", "defaultVal": 0.01}));
        node.addControl(new FloatControl(this.editor, "Emin", {"name": "Emin", "type": "Float", "defaultVal": -10}));
        node.addControl(new FloatControl(this.editor, "Emax", {"name": "Emax", "type": "Float", "defaultVal": 10}));
        node.addControl(new FloatControl(this.editor, "DeltaE", {"name": "DeltaE", "type": "Float", "defaultVal": 0.02}));
        var out0 = new Rete.Output("Parameter","Parameter", SocketGeneral);
        node.addOutput(out0);
        node.executor = {"path": "scinode.executors.built_in", "name": "PropertyToSocket", "type": "class"};
    
        return node
    }
}
class QEPseudo_SSSPComponent extends ScinodeComponent {

    constructor(){
        super("QEPseudo_SSSP");
        this.catalog = "QE";
        this.name = "Pseudo_SSSP";
    }

    builder(node) {
        this.init(node);
        node.meta.args = [];
        node.meta.kwargs = ['Pseudo'];
    
        node.addControl(new EnumControl(this.editor, "Pseudo", {"name": "Pseudo", "type": "Enum", "defaultVal": "SSSP_1.1.2_PBE_efficiency", "options": ["SSSP_1.1.2_PBE_efficiency", "SSSP_1.1.2_PBE_precision"]}));
        var out0 = new Rete.Output("Pseudo","Pseudo", SocketString);
        node.addOutput(out0);
        node.executor = {"path": "scinode.executors.built_in", "name": "PropertyToSocket", "type": "class"};
    
        return node
    }
}
class QEPWComponent extends ScinodeComponent {

    constructor(){
        super("QEPW");
        this.catalog = "QE";
        this.name = "PW";
    }

    builder(node) {
        this.init(node);
        node.meta.args = [];
        node.meta.kwargs = ['Directory', 'Structure', 'Kpoint', 'Pseudo', 'Parameter', 'Scheduler'];
    
        node.addControl(new StringControl(this.editor, "Directory", {"name": "Directory", "type": "String", "defaultVal": ""}));
        var inp0 = new Rete.Input("Structure","Structure", SocketGeneral);
        node.addInput(inp0);
        var inp1 = new Rete.Input("Kpoint","Kpoint", SocketGeneral);
        inp1.addControl(new FloatVectorControl(this.editor, "Kpoint", {"defaultVal": [1, 1, 1], "size": 3, "type": "FloatVector"}));
        node.addInput(inp1);
        var inp2 = new Rete.Input("Pseudo","Pseudo", SocketString);
        inp2.addControl(new StringControl(this.editor, "Pseudo", {"defaultVal": "", "type": "String"}));
        node.addInput(inp2);
        var inp3 = new Rete.Input("Parameter","Parameter", SocketGeneral);
        node.addInput(inp3);
        var inp4 = new Rete.Input("Scheduler","Scheduler", SocketGeneral);
        node.addInput(inp4);
        var out0 = new Rete.Output("Structure","Structure", SocketGeneral);
        node.addOutput(out0);
        var out1 = new Rete.Output("Energy","Energy", SocketGeneral);
        node.addOutput(out1);
        var out2 = new Rete.Output("Force","Force", SocketGeneral);
        node.addOutput(out2);
        var out3 = new Rete.Output("Calculator","Calculator", SocketGeneral);
        node.addOutput(out3);
        node.executor = {"path": "scinode_dft.qe.pw", "name": "PW", "type": "class"};
    
        return node
    }
}
class QEDosComponent extends ScinodeComponent {

    constructor(){
        super("QEDos");
        this.catalog = "QE";
        this.name = "Dos";
    }

    builder(node) {
        this.init(node);
        node.meta.args = [];
        node.meta.kwargs = ['directory', 'prefix', 'Calculator', 'Parameter', 'Scheduler'];
    
        node.addControl(new StringControl(this.editor, "directory", {"name": "directory", "type": "String", "defaultVal": ""}));
        node.addControl(new StringControl(this.editor, "prefix", {"name": "prefix", "type": "String"}));
        var inp0 = new Rete.Input("Calculator","Calculator", SocketGeneral);
        node.addInput(inp0);
        var inp1 = new Rete.Input("Parameter","Parameter", SocketGeneral);
        node.addInput(inp1);
        var inp2 = new Rete.Input("Scheduler","Scheduler", SocketGeneral);
        node.addInput(inp2);
        var out0 = new Rete.Output("Energies","Energies", SocketGeneral);
        node.addOutput(out0);
        var out1 = new Rete.Output("Dos","Dos", SocketGeneral);
        node.addOutput(out1);
        node.executor = {"path": "scinode_dft.qe.dos", "name": "Dos", "type": "class"};
    
        return node
    }
}
class QEProjwfcComponent extends ScinodeComponent {

    constructor(){
        super("QEProjwfc");
        this.catalog = "QE";
        this.name = "Projwfc";
    }

    builder(node) {
        this.init(node);
        node.meta.args = [];
        node.meta.kwargs = ['directory', 'prefix', 'Calculator', 'Parameter', 'Scheduler'];
    
        node.addControl(new StringControl(this.editor, "directory", {"name": "directory", "type": "String", "defaultVal": ""}));
        node.addControl(new StringControl(this.editor, "prefix", {"name": "prefix", "type": "String"}));
        var inp0 = new Rete.Input("Calculator","Calculator", SocketGeneral);
        node.addInput(inp0);
        var inp1 = new Rete.Input("Parameter","Parameter", SocketGeneral);
        node.addInput(inp1);
        var inp2 = new Rete.Input("Scheduler","Scheduler", SocketGeneral);
        node.addInput(inp2);
        var out0 = new Rete.Output("Energies","Energies", SocketGeneral);
        node.addOutput(out0);
        var out1 = new Rete.Output("Pdos","Pdos", SocketGeneral);
        node.addOutput(out1);
        node.executor = {"path": "scinode_dft.qe.projwfc", "name": "Projwfc", "type": "class"};
    
        return node
    }
}
class ASEReadStructureComponent extends ScinodeComponent {

    constructor(){
        super("ASEReadStructure");
        this.catalog = "ASE";
        this.name = "ReadStructure";
    }

    builder(node) {
        this.init(node);
        node.meta.args = [];
        node.meta.kwargs = ['file'];
    
        node.addControl(new FileControl(this.editor, "file", {"name": "file", "type": "File"}));
        var out0 = new Rete.Output("Structure","Structure", SocketGeneral);
        node.addOutput(out0);
        node.executor = {"path": "scinode_atoms.io.read", "name": "read_structure_from_file_js", "type": "function"};
    
        return node
    }
}
class ASEScaleCellComponent extends ScinodeComponent {

    constructor(){
        super("ASEScaleCell");
        this.catalog = "ASE";
        this.name = "ScaleCell";
    }

    builder(node) {
        this.init(node);
        node.meta.args = [];
        node.meta.kwargs = ['scale_atoms', 'scale', 'structure'];
    
        node.addControl(new BoolControl(this.editor, "scale_atoms", {"name": "scale_atoms", "type": "Bool"}));
        var inp0 = new Rete.Input("structure","structure", SocketGeneral);
        node.addInput(inp0);
        var inp1 = new Rete.Input("scale","scale", SocketGeneral);
        inp1.addControl(new FloatVectorControl(this.editor, "scale", {"size": 3, "type": "FloatVector"}));
        node.addInput(inp1);
        var out0 = new Rete.Output("Structure","Structure", SocketGeneral);
        node.addOutput(out0);
        node.executor = {"path": "scinode_atoms.operators.scale_cell", "name": "scale_cell", "type": "function"};
    
        return node
    }
}
class MathVector3DComponent extends ScinodeComponent {

    constructor(){
        super("MathVector3D");
        this.catalog = "Math";
        this.name = "Vector3D";
    }

    builder(node) {
        this.init(node);
        node.meta.args = [];
        node.meta.kwargs = ['x', 'y', 'z'];
    
        var inp0 = new Rete.Input("x","x", SocketGeneral);
        inp0.addControl(new FloatControl(this.editor, "x", {"type": "Float"}));
        node.addInput(inp0);
        var inp1 = new Rete.Input("y","y", SocketGeneral);
        inp1.addControl(new FloatControl(this.editor, "y", {"type": "Float"}));
        node.addInput(inp1);
        var inp2 = new Rete.Input("z","z", SocketGeneral);
        inp2.addControl(new FloatControl(this.editor, "z", {"type": "Float"}));
        node.addInput(inp2);
        var out0 = new Rete.Output("Result","Result", SocketFloat);
        node.addOutput(out0);
        node.executor = {"path": "scinode_math.input.vector", "name": "vector3d", "type": "function"};
    
        return node
    }
}
class NumpyLinspaceComponent extends ScinodeComponent {

    constructor(){
        super("NumpyLinspace");
        this.catalog = "Numpy";
        this.name = "Linspace";
    }

    builder(node) {
        this.init(node);
        node.meta.args = ['start', 'stop'];
        node.meta.kwargs = ['num'];
    
        var inp0 = new Rete.Input("start","start", SocketGeneral);
        inp0.addControl(new FloatControl(this.editor, "start", {"type": "Float"}));
        node.addInput(inp0);
        var inp1 = new Rete.Input("stop","stop", SocketGeneral);
        inp1.addControl(new FloatControl(this.editor, "stop", {"type": "Float"}));
        node.addInput(inp1);
        var inp2 = new Rete.Input("num","num", SocketGeneral);
        inp2.addControl(new FloatControl(this.editor, "num", {"type": "Float"}));
        node.addInput(inp2);
        var out0 = new Rete.Output("Result","Result", SocketGeneral);
        node.addOutput(out0);
        node.executor = {"path": "numpy", "name": "linspace", "type": "function"};
    
        return node
    }
}
class MathpowerComponent extends ScinodeComponent {

    constructor(){
        super("Mathpower");
        this.catalog = "Math";
        this.name = "power";
    }

    builder(node) {
        this.init(node);
        node.meta.args = ['x', 'y'];
        node.meta.kwargs = [];
    
        var inp0 = new Rete.Input("x","x", SocketFloat);
        inp0.addControl(new FloatControl(this.editor, "x", {"defaultVal": 1, "type": "Float"}));
        node.addInput(inp0);
        var inp1 = new Rete.Input("y","y", SocketFloat);
        inp1.addControl(new FloatControl(this.editor, "y", {"defaultVal": 2, "type": "Float"}));
        node.addInput(inp1);
        var out0 = new Rete.Output("Result","Result", SocketFloat);
        node.addOutput(out0);
        node.executor = {"path": "Math", "name": "pow", "type": "function"};
    
        return node
    }
}
var json_components = [new TemplateTestComponent(), 
new QEPWParameterComponent(), 
new QEDosParameterComponent(), 
new QEProjwfcParameterComponent(), 
new QEPseudo_SSSPComponent(), 
new QEPWComponent(), 
new QEDosComponent(), 
new QEProjwfcComponent(), 
new ASEReadStructureComponent(), 
new ASEScaleCellComponent(), 
new MathVector3DComponent(), 
new NumpyLinspaceComponent(), 
new MathpowerComponent(), 
];