
window.onload = function() {
    fix_code_blocks()
};  

function save_data(values) {
    var update = []
    values.forEach(element => {
        update.push({
            "key": element,
            "value": document.getElementById(element).value
        });
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

function update_card(values) {
    apicall("/api/config", function(ret) {
        values.forEach(element => {
            if (ret.config[element]) {
                document.getElementById(element).value = ret.config[element];
            }
        });
    });
}

function update_card_str(values_text) {
    update_card(values_text.split(","));
}
