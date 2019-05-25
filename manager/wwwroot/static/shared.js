function apicall(url, callback) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var ret = JSON.parse(this.responseText);
            callback(ret);
        }
    };
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
  }

function update_menu_badges() {

    apicall("/api/ansible", function(ret) {
        menu_id = "menu-provision";
        if (ret.running) {
            document.getElementById(menu_id).style.textTransform = "uppercase";
        } else {
            document.getElementById(menu_id).style.textTransform = "none";
        }
    });

}
