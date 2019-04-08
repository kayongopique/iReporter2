
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
            addRow('usertable', response.incidentType,response.location,response.comment,current_flag);
        }
    })
}

function addRow(tableid,incidentType,location,comment,redflagid){
    let newrow = document.getElementById(tableid).insertRow(-1);

    let new_incident = document.createTextNode(incidentType);
    let its_location = document.createTextNode(location);
    let its_comment = document.createTextNode(comment);

    var button1 = document.createElement('button');
    button1.innerHTML ='edit location';
     button1.addEventListener('click', ()=>{
    document.getElementById('presentlocation').innerHTML =
    `<input type="text" onblur = updateLocation(event, ${redflagid}) id ="edit" required>`;
    button2.innerHTML= 'save'
     });

    var button2 = document.createElement('button');
    button2.innerHTML = 'edit comment';
    button2.addEventListener('click', ()=> {
    document.getElementById('presentcommet').innerHTML =
    `<input type="text" onblur = updateComment(event, ${redflagid}) id ="edit" required>`;
    button2.innerHTML= 'save';
    });


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
            data = response.redflag;
             document.getElementById('incidentType').innerText=data.incidentType;
             document.getElementById('location').innerText= data.location;
             document.getElementById('comment').innerText =data.comment;
             document.getElementById('status').innerText =data.status;
             document.getElementById('commentbtn').appendChild(button2);
             document.getElementById('locationbtn').appendChild(button1);
        })
    });
    
    newrow.insertcell(0).appendChild(new_incident);
    newrow.insertcell(1).appendChild(its_location);
    newrow.insertcell(2).appendChild(its_comment);
    newrow.insertcell(3).appendChild(button);


}

function updateLocation(e, redflagid){
    const locationurl = 'http://127.0.0.1:5000/api/v1/redflag/${redflagid}/location';
    newlocation= e.target.value;
     let data = {
        location : newlocation
     }

     fetch(locationurl,{
         method: "PATCH",
         mode : "cors",
         headers : {
             'Content-Type': 'Application/json', 'Authorization':'Bearer ${token}', 'x-access-token':'${token}' 
         },

         body : JSON.stringify(data)
     }).then(res =>res.json())
     .then(response =>{
         alert(response.message);
         document.location.reload(true);
     })
}

function updateComment(e, redflagid){
    const commenturl = 'http://127.0.0.1:5000/api/v1/redflag/${redflagid}/comment';
    newcomment= e.target.value;
     let data = {
         presentcomment : newcomment
     }

     fetch(commenturl,{
         method: "PATCH",
         mode : "cors",
         headers : {
             'Content-Type': 'Application/json', 'Authorization':'Bearer ${token}', 'x-access-token':'${token}' 
         },

         body : JSON.stringify(data)
     }).then(res =>res.json())
     .then(response =>{
         alert(response.message);
         document.location.reload(true);
     })
}

