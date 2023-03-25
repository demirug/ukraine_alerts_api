function formatDuration(timestamp) {
    let out = "";

    days = Math.floor(timestamp / (24 * 60 * 60 * 1000));
    if (days > 0) {
        timestamp -= days * 24 * 60 * 60 * 1000;
        out += days + " d. ";
    }

    hours = Math.floor(timestamp / (60 * 60 * 1000));
    if (hours > 0) {
        timestamp -= hours * 60 * 60 * 1000;
        out += hours + " h. ";
    }

    minutes = Math.floor(timestamp / (60 * 1000));
    if (minutes > 0) {

        timestamp -= minutes * 60 * 1000;
        out += minutes + " min. ";
    }
    if (out == "") {
        out += " < 1 minute"
    }

    return out;
}

function formatTime(timestamp) {
    let date = new Date(timestamp);
    return new Intl.DateTimeFormat("en-US", {
          year: "numeric",
          month: "numeric",
          day: "numeric",
          hour: "numeric",
          minute: "numeric",
          second: "numeric",
          hour12: false
      }
  ).format(date);
}

function showModal(elm_id, elm_name="None") {

    const xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/history/' + elm_id + '?limit=10');
    xhr.responseType = 'json';
    xhr.onload = function(e) {
      if (this.status == 200) {
        let modal = new MainModal();
        modal.setTitle(elm_name + " alert history");

        if(this.response.length > 1) {
            let id = 0;
            for(var el of this.response) {
              if(el['is_alert']) {
                if(id != 0) {
                    modal.addToBody("<hr>")
                } else id++;
                if(el['end_timestamp'] == null) {
                  modal.addToBody("<p>Period: " + formatTime(el['timestamp']) +  " -- NOW</p>")
                } else {
                  modal.addToBody("<p>Period: " + formatTime(el['timestamp']) + " -- " + formatTime(el['end_timestamp']) +  "</p>")
                  modal.addToBody("<p>Alarm duration: " + formatDuration(new Date(el['end_timestamp']) - new Date(el['timestamp'])) +  "</p>")
                }

              }
            }
        } else {
             modal.addToBody("<h5>History not found</h5>")
        }

        modal.addFooterCloseButton().show();
      }
    };
xhr.send();
}

for(let elm of document.querySelectorAll("[class^='region']")) {
    elm.addEventListener('click', function() {
      showModal(elm.classList[0].slice(7), elm.getAttribute('reg_name'));
    })
}