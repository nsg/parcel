function apicall(url, callback) {
    $.getJSON(url, callback);
}

// If someone finds a way to do this in CSS, please open a issue/PR
function fix_code_blocks() {
    document.querySelectorAll("code").forEach(el =>
        el.textContent = el.textContent.replace(/^\n/,'')
    );
}
