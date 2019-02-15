token = localStorage.getItem('access-token');
const flagurl = 'http://127.0.0.1:5000/api/v1/redflags';

const userflagurl = 'http://127.0.0.1:5000/api/v1/user/redfalgs';

function create_incident(){
    let incidentType = document.getElementById('incidentType').value;
    let location =document.getElementById('location').value;
    let comment =document.getElementById('comment').value;

    let data ={
        incidentType:incidentType,
        location:location,
        comment:comment
    }
    fetch(flagurl, {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'Application/json', 'Authorization':'Bearer ${token}', 'x-access-token':'${token}'
        },
        body:JSON.stringify(data)

    }).then(res=>res.json())
    .then(response=> {
        current_flag = response.redfalg.id;
        if (response.message == 'created redflag'){
            addRow('usertable', incidentType,location,comment,current_flag);
        }
    })
}

function addRow(tableid,incidentType,location,comment,redflagid){
    let newrow = document.getElementById(tableid).insertRow(-1);

    let new_incident = document.createTextNode(incidentType);
    let its_location = document.createTextNode(location);
    let its_comment = document.createTextNode(comment);

    var button = document.createElement('button');
    button.innerHTML= "Details";

    button.addEventListener('click', ()=>{
        const specificurl = 'http://127.0.0.1:5000/api/v1/redflag/${redflagid}';

        fetch(flagurl, {
            method: 'GET',
            mode: 'cors',
            headers: {
                'Content-Type': 'Application/json', 'Authorization':'Bearer ${token}', 'x-access-token':'${token}'
            }
        }).then(res =>json())
        .then(response =>{
            data = response.redflag
             document.getElementById('incidentType').innerText=data.incidentType;
             document.getElementById('location').innerText= data.location;
             document.getElementById('comment').innerText =data.comment;
             document.getElementById('status').innerText =data.status;
             document.getElementById('statusbtn').appendChild(button1);
             document.getElementById('locationbtn').appendChild(button2);
        })
    });
    
    newrow.insertcell(0).appendChild(new_incident);
    newrow.insertcell(1).appendChild(its_location);
    newrow.insertcell(2).appendChild(its_comment);
    newrow.insertcell(3).appendChild(button);


}
