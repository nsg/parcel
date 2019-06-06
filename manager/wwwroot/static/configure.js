
window.onload = function() {
    fix_code_blocks()
};  

function get_config() {
    apicall("/api/config", function(ret) {
        console.log(ret);
    });
}

function save_lxd_config() {
    var remote = document.getElementById("lxd-remote");
    var password = document.getElementById("lxd-password");

    console.log(submit.parentNode);

    return false;
}
