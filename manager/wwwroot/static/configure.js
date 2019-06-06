
window.onload = function() {
    fix_code_blocks()
};  

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

function update_card_lxd_socket() {
    apicall("/api/config", function(ret) {
        if (ret.config['lxd-remote']) {
            document.getElementById("lxd-remote").value = ret.config['lxd-remote'];
        }
        if (ret.config['lxd-password']) {
            document.getElementById("lxd-password").value = ret.config['lxd-password'];
        }
    });
}
