
window.onload = function() {
    fix_code_blocks()
};  

function append_err(obj, err) {
    let p = document.createElement("p");
    p.innerText = err;
    obj.style.display = "block";
    obj.appendChild(p);
}

function save_data(save_button, values_str) {
    let orig_save_button_string = "Validate & Save";
    save_button.classList.add("button-saving");
    save_button.innerHTML = "Saving ..."
    var values = values_str.split(",");
    var abort = false;

    let err_div = save_button.parentNode.parentNode.getElementsByClassName("form-error-message")[0]
    err_div.style.display = "none";
    err_div.innerHTML = "";

    values.forEach(element => {
        let msg = validate(element, document.getElementById(element).value);
        if (msg[0]) {
            document.getElementById(element).classList.remove("is-invalid");
            document.getElementById(element).classList.add("is-valid");
        } else {
            document.getElementById(element).classList.remove("is-valid");
            document.getElementById(element).classList.add("is-invalid");
            save_button.classList.remove("button-saving");
            save_button.classList.remove("btn-primary");
            save_button.classList.add("btn-danger");
            save_button.innerHTML = "Invalid configuration, not saved!"
            msg[1].forEach(emsg => {
                append_err(err_div, emsg)
            });
            abort = true;
        }
    });

    if (abort) {
        return false;
    }

    save_button.classList.remove("btn-danger");
    save_button.classList.add("btn-primary");

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
            save_button.innerHTML = orig_save_button_string;
        }, 1000);
    });

    return false;
}

function validate(field, data) {
    let msg = [];

    // Server side validations
    $.ajax({
        type: "POST",
        url: "/api/validate",
        data: JSON.stringify({"field": field, "data": data}),
        success: null,
        contentType : 'application/json',
        async: false
    }).done(function(ret) {
        ret.forEach(element => {
            msg.push(element)
        });
    });

    // Client side validations
    switch(field) {
        case "origin":
            if (data.match(/[, ]/)) msg.push("Origin must be a valid single domain/FQDN.");
            break;
        case "domains":
            if (data.match(/example\.com/)) msg.push("Please use a real domain, example.com is for examples.")
            if (data.match(/[ ]/)) msg.push("Spaces are not allowed in domains.")
            if (data.match(/[,]$/)) msg.push("Remove last \",\" from domains.")
            break;
        case "email-accounts":
            if (!data.match(/^([^:,@]+@[^:,@]+:[^:,@]+,?)+$/)) msg.push("Incorrenct format!");
            break;
    }

    return [msg.length == 0, msg];
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
