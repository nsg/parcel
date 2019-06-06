
window.onload = function() {
    fix_code_blocks()
};  

function get_config() {
    apicall("/api/config", function(ret) {
        console.log(ret);
    });
}
