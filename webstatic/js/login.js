const url = "http://localhost:5000/learnplus/home/login"

document.querySelector(".username").addEventListener("click", ()=> {
 if (document.querySelector(".user").id == "") {
    document.querySelector(".login").style.visibility = 'visible';
 } else {
   alert("return account info page")
  }});

document.querySelector(".usrimg").addEventListener("click", ()=> {
  if (document.querySelector(".user").id == "") {
    document.querySelector(".login").style.visibility = 'visible';
  } else {
    alert("return account info page")
  }});
let usernameError = document.createElement('div')
usernameError.id = 'usernameError'
usernameError.textContent='Enter Username'
usernameError.className = 'logerror'

let passwordError = document.createElement('div')
passwordError.id = 'passwordError'
passwordError.textContent = "Enter Password"
passwordError.className = 'logerror'

async function loginRequest(username, password) {
 let Url = url + "?" + "username=" + username +"&" + "password=" + password;
  console.log(Url)
  try {
    const response = await fetch(Url, {"headers":{"Accept":"application/json"}});
    if (!response.ok) {
      if (response.status == 404) {
         usernameError.textContent = "Not found, Invalid username"
         document.querySelector("#logform").insertBefore(usernameError, document.querySelector("#logform").children[1])
         try {
          document.querySelector("#logform").removeChild(passwordError)
         } catch  (error) {
           //pass
         }
      } else{
         passwordError.textContent = "Unauthorized, password Error"
         document.querySelector("#logform").insertBefore(passwordError, document.querySelector("#logform").children[1])
      }
      throw new Error(`Response status: ${response.status}`);
    }
    json = await response.json()
    //update use img, username and id
    document.querySelector(".username").textContent = json['username']
    document.querySelector(".usrimg").src = json['imgURL']
    document.querySelector(".login").style.visibility = "hidden";
    document.querySelector(".user").id = json.uid
    //dom 
    //insert units
    if (json.enrolled.length != 0) {
       document.querySelector(".enrolled").removeChild(document.querySelector(".enrolled").firstElementChild)
       document.querySelector(".enrolled").appendChild(document.createElement("ul"))
       for (entry of json.enrolled) {
        _entry = document.createElement("li")
        _entry.id = entry.id
        _entryname = document.createElement("div")
        _entryname.textContent = entry.name
        _entry.appendChild(_entryname)
        _entryprogress = document.createElement("div")
        _entryprogress.textContent = "progress: " + entry.progress
        _entry.appendChild(_entryprogress)
        document.querySelector(".enrolled > ul").appendChild(_entry)
      }
    } else {
        document.querySelector(".enrolled > a").textContent = "No record"
    }

    //insert schedule
    if (json.schedule.length != 0) {
        document.querySelector(".upnext").removeChild(document.querySelector(".upnext").firstElementChild)
        document.querySelector(".upnext").appendChild(document.createElement("ul"))
        for (entry of json.schedule) {
           _entry = document.createElement("li")
           _entry.id = entry.id
           _entryname = document.createElement("div")
           _entryname.textContent = entry.name
           _entry.appendChild(_entryname)
           _entrytime = document.createElement("div")
           _entrytime.textContent = "Time:" + entry.Time
           _entry.appendChild(_entrytime)
           document.querySelector(".upnext ul").appendChild(_entry)
        }
    } else {
        document.querySelector(".upnext > a").textContent = "No record"
    }
    //last studies
    if (json.lastStudied != null) {
        document.querySelector("#last").lastElementChild.textContent = json.lastStudied
    }
    //schedule -- next
    if (json.scheduled.length != 0) {
        x = document.querySelectorAll("#next span")
        x[0].textContent = "Unit:" + json.scheduled.name
        x[1].textContent = "Time:" + json.scheduled.Time
    }
  } catch (error) {
    console.error(error.message);
  }
}


document.querySelector('#login').addEventListener('click', ()=> {
 if (document.querySelector('#usernme').value == "") {
    document.querySelector("#logform").insertBefore(usernameError, document.querySelector("#logform").children[1]);
 } else {
   if (document.querySelector('#password').value == '') {
     document.querySelector("#logform").insertBefore(passwordError, document.querySelector("#logform").children[1]);
   } else {
      username = document.querySelector("#usernme").value.trim();
      password = document.querySelector("#password").value
      try {
          document.querySelector('.login').removeChild(passwordError);
      } catch (e) {
        //pass
      } finally {
         loginRequest(username, password)
      }
    }
   }
  }
);

document.querySelector('#usernme').addEventListener('keydown', ()=> {
  try {
    document.querySelector('#logform').removeChild(usernameError)
  } catch (e) {
   //pass
  }
});
document.querySelector('#password').addEventListener('keydown', ()=> {
  try {
    document.querySelector('#logform').removeChild(passwordError)
  } catch (e) {
   //pass
  }
});

//reload()
