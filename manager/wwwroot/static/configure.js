
window.onload = function() {
    setInterval(update_menu_badges, 10000);
    update_menu_badges();
    fix_code_blocks()
};  

function get_config() {
    apicall("/api/config", function(ret) {
        console.log(ret);
    });
}
