var container = document.querySelector('#rete');
// var editor = new Rete.NodeEditor('scinode@0.1.0', container);
var editor = new ScinodeEditor('scinode@0.1.0', container);
editor.use(ConnectionPlugin.default);
editor.use(VueRenderPlugin.default);
editor.use(ContextMenuPlugin.default, {
    delay: 0,
    allocate(component) {
        return [component.catalog]
    },
    rename(component) {
        return component.name;
    },
});
editor.use(AreaPlugin);
editor.use(CommentPlugin.default);
editor.use(HistoryPlugin);
editor.use(ConnectionMasteryPlugin.default);
editor.use(MinimapPlugin.default);
// editor.use(MinimapPlugin);
var engine = new Rete.Engine('scinode@0.1.0');
// register all nodes
components.map(c => {
    editor.register(c);
    engine.register(c);
});
json_components.map(c => {
    editor.register(c);
    engine.register(c);
});
editor.on('process nodecreated noderemoved connectioncreated connectionremoved', async () => {
    console.log('process');
    await engine.abort();
    // await engine.process(editor.toJSON());
});
