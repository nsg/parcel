
window.onload = function() {
    fix_code_blocks()
};  

function save_data(save_button, values_str) {
    save_button.classList.add("button-saving");
    save_button.innerHTML = "Saving ..."
    var values = values_str.split(",");

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
    }).done(function() {
        setTimeout(function() {
            save_button.classList.remove("button-saving");
            save_button.innerHTML = "Save";
        }, 1000);
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
