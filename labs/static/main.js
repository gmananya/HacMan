//  make api call when button is clicked

function log_activity(msg){
    // logger = document.getElementById('logs');
    // let message = document.createElement('p');
    // message.innerHTML = msg;
    // logger.appendChild(message);
}

// function getData() {

//     fetch('/api/list/')
//     .then(res => {return res.json(); 
//     })
//     .then(data => {
//         document.getElementById('content').innerHTML = ""
//         for (let i = 0; i < data.length; i++) {
//             console.log(data[i].name);

//             // append a child to the div
//             let lab = document.createElement('p');
//             lab.className = "lab";
//             lab.id = data[i].id;
//             lab.innerHTML += "LAB : ";
//             lab.innerHTML += data[i].name;

//             lab.innerHTML += `<button onClick="start_lab(${data[i].id})"> start </button>`
//             lab.innerHTML += `<button onClick="stop_lab(${data[i].id})"> stop </button>`
//             lab.innerHTML += data[i].name + " " + data[i].status + '<br><hr>';
            
//             document.getElementById('content').appendChild(lab);
//         }
//          log_activity("refreshed UI");
//         }
//         )
//     .catch(err => console.error(err));

//     // get element by id content
    

// }

function start_lab(lab_id) {
    alert("Starting lab" + lab_id);
    fetch('/api/start/' + lab_id + '/')
    .then(res => {return res.json();})
    .then(data => {
        console.log(data);
        log_activity(data.container_id + " started");
        // getData();
        // reload html page
        window.location.reload();
        document.getElementsByClassName('modal_header_text')[0].innerHTML = data.name;
        document.getElementsByClassName('modal-body')[0].innerHTML = data.container_id;
        modal.style.display = "block";
    }
    )
    .catch(err => console.error(err));
    // reload page after 3 seconds
    setTimeout(function(){window.location.reload();}, 3000);

}

function stop_lab(lab_id) {
    alert("Stop lab" + lab_id);
    fetch('/api/stop/' + lab_id + '/')
    .then(res => {return res.json();})
    .then(data => {
        console.log(data);

        log_activity(data.container_id + " stopped");
        window.location.reload();


        // getData();
    }
    )
    .catch(err => console.error(err));
}

// run function on page load
// getData();

function prune_containers() {
    fetch('/api/prune_containers/')
    .then(res => {return res.json();})
    .then(data => {
        console.log(data);

        log_activity(data.container_id + " stopped");
        window.location.reload();


        // getData();
    }
    )
    .catch(err => console.error(err));
}