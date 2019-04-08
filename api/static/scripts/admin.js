token = localStorage.getItem('access-token');
const flagurl = 'http://127.0.0.1:5000/api/v1/redflags';

const userflagurl = 'http://127.0.0.1:5000/api/v1/user/redfalgs';

function get_incident(){
   
    fetch(flagurl, {
        method: 'GET',
        mode: 'cors',
        headers: {
            'Content-Type': 'Application/json', 'Authorization':'Bearer ${token}', 'x-access-token':'${token}'
        },
        body:JSON.stringify(data)

    }).then(res=>res.json())
    .then(response=> {
        current_flag = response.redfalg.id;
        if (response.status == 200){
            addRow('Admintable', incidentType,location,comment,current_flag);
        }
    })
}

function addRow(tableid,incidentType,location,comment,redflagid){
    let newrow = document.getElementById(tableid).insertRow(-1);

    let new_incident = document.createTextNode(incidentType);
    let its_location = document.createTextNode(location);
    let its_comment = document.createTextNode(comment);

    var button1 = document.createElement('button');
    button1.innerHTML ='reject';
    button1.addEventListener('click', ()=>{
    updatestatus('rejected',redflagid);
    // document.getElementById('presentstatus').innerHTML =
    // `<input type="text" onblur = updateLocation(event, ${redflagid}) id ="edit" required>`;
    button1.innerHTML= 'rejected'
    button2.style= `display : none`
     });

    // var button2 = document.createElement('button');
    // button2.innerHTML = 'edit comment';
    // button2.addEventListener('click', ()=> {
    // document.getElementById('presentcommet').innerHTML =
    // `<input type="text" onblur = updateComment(event, ${redflagid}) id ="edit" required>`;
    // button2.innerHTML= 'save';
    // });


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
             document.getElementById('date').innerText = data.registered_date;
             document.getElementById('user').innerText = data.createdby;
        })
    });
    
    newrow.insertcell(0).appendChild(new_incident);
    newrow.insertcell(1).appendChild(its_location);
    newrow.insertcell(2).appendChild(its_comment);
    newrow.insertcell(3).appendChild(button);
    newrow.insertcell(4).appendChild(button1);


}


function updatestatus(status,redflagid){
    const statusurl = 'http://127.0.0.1:5000/api/v1/redflag/${redflagid}/status';
    newstatus= status ;
     let data = {
         status : newstatus
     }

     fetch(statusurl,{
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

