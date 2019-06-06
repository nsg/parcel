
window.onload = function() {
    fix_code_blocks()
};  

function get_config() {
    apicall("/api/config", function(ret) {
        console.log(ret);
    });
}

function save_lxd_config() {
    var update = []

    update.push({
        "key": "lxd-remote",
        "value": document.getElementById("lxd-remote").value
    });

    update.push({
        "key": "lxd-password",
        "value": document.getElementById("lxd-password").value
    });

    $.ajax({
        type: "POST",
        url: "/api/config",
        data: JSON.stringify({"update": update}),
        success: null,
        contentType : 'application/json'
    });

    return false;
}
