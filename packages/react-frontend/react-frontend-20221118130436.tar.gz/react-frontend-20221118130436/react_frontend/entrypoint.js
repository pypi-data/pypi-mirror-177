
try {
    new Function("import('/reactfiles/frontend/main.8bf82215.js')")();
} catch (err) {
    var el = document.createElement('script');
    el.src = '/reactfiles/frontend/main.8bf82215.js';
    el.type = 'module';
    document.body.appendChild(el);
}
