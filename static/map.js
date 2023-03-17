function update_elements(data) {
      for(let obj of data) {
         let x = document.getElementsByClassName("region_" + obj['region_id'])
         for(let i = 0; i < x.length; i++) {
             x[i].style.fill = obj['is_alert'] ? "rgb(255, 0, 0)" : "rgb(50, 205, 50)"
         }
      }
}

function update_data(url_prefix="") {
   let xhr = new XMLHttpRequest();
   xhr.open('GET', url_prefix+ "/api/status", true);
   xhr.responseType = 'json';
   xhr.onload = function() {
       if(xhr.status === 200) {
           update_elements(xhr.response)
       }
   }
   xhr.send();
}