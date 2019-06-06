
var running_state = null

function trigger() {
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open("POST", "/api/ansible", true);
  xmlhttp.send();
  writeMessage("Provision will be trigged in a few seconds.");

  return false;
}

window.onload = function() {
  apicall("/api/ansible", function(ret) {

    if (ret.running) {
      writeMessage("Provision is running, status will update when it's completed.");
    }

    if (Object.keys(ret.data).length > 0) {
      render_stats(ret.data.stats);
      render_plays(ret.data.plays);
    } else {
      writeMessage("Provision is running, come back here in a minute or so...");
    }

    if (document.getElementById("ansible-messages").innerHTML == "") {
      document.getElementById("ansible-messages").style.display = "none";
    } else {
      document.getElementById("ansible-messages").style.display = "block";
    }
  });

  setInterval(detect_trigger_changes, 10000);
};

function detect_trigger_changes() {
  apicall("/api/ansible", function(ret) {
    if (running_state == null) {
      running_state = ret.running;
    } else if (ret.running != running_state) {
      location.reload();
    }
  });
}

function render_plays(plays) {
  plays.forEach(function(play) {
    var h5 = document.createElement("h5");
    h5.innerHTML = play.play.name;
    document.getElementById("ansible-log").appendChild(h5);
    play.tasks.forEach(function(task) {
      var h6 = document.createElement("h6");
      h6.innerHTML = task.task.name;
      document.getElementById("ansible-log").appendChild(h6);
      Object.keys(task.hosts).forEach(function(host) {
        var badge = document.createElement("span");
        badge.classList.add("badge");
        badge.style.marginLeft = "0.5em";
        var h = task.hosts[host];

        if (h.changed) {
          badge.classList.add("badge-primary");
          badge.innerHTML = host;
        } else if (h.failed) {
          badge.classList.add("badge-danger");
          if (h.msg) {
            writeMessage("Task '" + task.task.name + "' failed for host " + host);
            writeMessage(h.msg);
          }
          badge.innerHTML = host;
        } else {
          badge.classList.add("badge-success");
          badge.innerHTML = host;
        }
        h6.appendChild(badge);
      });
    });
  });
}

function render_stats(stats) {
  Object.keys(stats).forEach(function(container) {
    const {
      changed,
      failures,
      ok,
      skipped,
      unreachable
    } = stats[container];

    var badge = document.createElement("span");
    badge.innerHTML = container;
    badge.classList.add("badge");
    badge.classList.add("badge-pill");
    badge.style.marginRight = "0.4em";
    if (failures > 0 || unreachable > 0) {
      badge.classList.add("badge-danger");
      writeMessage("Provision of " + container + " failed, please investigate.");
    } else if (changed > 0) {
        badge.classList.add("badge-primary");
        writeMessage("Changes have been applied to " + container);
    } else {
      badge.classList.add("badge-success");
    }

    document.getElementById("ansible").appendChild(badge);
  });
}

function writeMessage(msg) {
  document.getElementById("ansible-messages").innerHTML =
    document.getElementById("ansible-messages").innerHTML + msg + "<br>";
}
