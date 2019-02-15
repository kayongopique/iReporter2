// document.getElementById('summit_btn').addEventListener('click',Signup())
function Signup(){
    let firstname = document.getElementById('firstname').value;
    let lastname = document.getElementById('lastname').value;
    let othernames = document.getElementById('othersnames').value;
    let email = document.getElementById('email').value;
    let tel = document.getElementById('tel').value;
    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;
    
    // if (password1 !=password2){
    //     alert('password do not match');
    //     return;
    // }
    const url = 'http://127.0.0.1:5000/api/v1/user/register';
    let data = {
        firstname:firstname,
        lastname:lastname,
        othernames:othernames,
        username:username,
        password:password,
        tel:tel,
        email:email
        
    }

    fetch(url, {
        method : 'POST',
        mode : 'cors',
        headers: {
            'Content-Type': 'Application/json'  }, 
            // 'Authorization': 'Bearer ${token}', 'x-access-token':'${token}'
     
        body : JSON.stringify(data)

    }).then(res =>res.json())
    .then(response=>{
        alert(response.message);
        if(response.message=='user has been registered'){
            window.location.replace('login.html');
        }
    })

}
function login(){
    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;

    const url = 'http://127.0.0.1:5000/api/v1/user/login';

    let data ={
        username:username,
        password:password
    }
    fetch(url, {
        method:'POST',
        mode:'cors',
        headers:{
            'Content-Type': 'Application/json'
        },
        body:JSON.stringify(data)
    }).then(res=>res.json())
    .then(response=>{
        localStorage.setItem("access-token", response.token);
        if(response.message=='youve logged in'){
            redirectTo(response.IsAdmin);
        }else
        {
            if(response.message== 'user not found'){
            alert('please sign up');
            window.location.replace('index.html');
        }else{
            window.location.reload();
             
        }
    }
    })
    function redirectTo(boolen){
        // if (boolen == false){
            window.location.replace('redflag.html');
        // }else{
        //     window.location.replace('admin.html');
        // }
    }
}