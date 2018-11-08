function klik() {
    alert("alohamora beybeh");
}

function signUp(){
    // debugger
    username = document.getElementById('username').value;
    email = document.getElementById('email').value;
    fullname = document.getElementById('full-name').value;
    password = document.getElementById('password').value;

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("POST", "http://localhost:5000/signup");
    xmlHttp.setRequestHeader("Content-Type", "application/json");
    xmlHttp.send(JSON.stringify({
        "username": username,
        "email": email,
        "password": password,
        "fullname": fullname
    }));
    xmlHttp.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 201){
            alert("Data Berhasil Di Submit dengan Status Code: "+this.status);
            window.location = "/login.html";
        }
        else if(this.readyState == 4){
            alert("Data gagal di input: "+this.status);
        }
    };
}

function signIn(){
    // debugger
    email = document.getElementById("email").value;
    password = document.getElementById("password").value;

    var xmlRequest = new XMLHttpRequest();
    xmlRequest.open("POST", "http://localhost:5000/login");
    xmlRequest.setRequestHeader("Content-Type", "application/json");
    xmlRequest.send(JSON.stringify({
        "email": email,
        "password": password
    }));
    xmlRequest.onreadystatechange = function(){
        // alert(this.response)
        if(this.readyState == 4 && this.status == 200){
            // alert(this.response)
            // localStorage.setItem('email', this.response);
            // localStorage.setItem('username', this.response);
            // localStorage.setItem('password', this.response);
            document.cookie="email="+this.response;
            window.location = "/timeline.html";
        }
        else if(this.readyState == 4){
            alert("SignIn gagal dengan status code :"+this.status);
        }
    };
}
function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function getProfile(){
    // username = localStorage.getItem('username')
    // alert(username)
    var xmlProfile = new XMLHttpRequest();
    xmlProfile.open("POST", "http://localhost:5000/getProfile");
    // xmlProfile.setRequestHeader("Content-Type","application/json");
    xmlProfile.setRequestHeader("Authorization", getCookie("email"))
    xmlProfile.send()
    // xmlProfile.send(JSON.stringify({
    //     "username":username
    // }));
    xmlProfile.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200){
            profile = JSON.parse(this.response)
            alert(this.response)
            document.getElementById("profile-fullname").innerText = (profile.fullname)
            document.getElementById("profile-foto").src = profile.photoprofile
            document.getElementById("nav-pic").src = profile.photoprofile
            document.getElementById("tweet-pic").src = profile.photoprofile
            document.getElementById("user-name").innerText = (profile.username)
            document.getElementById("bio").innerText = (profile.bio)
        }
    }
}
function addTweet(){
    var xmlHttp = new XMLHttpRequest();
    tweet = document.getElementById('posttweetta').value;    
    xmlHttp.open("POST","http://localhost:5000/tweeting");
    xmlHttp.setRequestHeader("Content-Type", "application/json");
    xmlHttp.send(JSON.stringify({
        "tweet": tweet,
        "username" : localStorage.getItem('username')
    }));
    xmlHttp.onreadystatechange = function(){
        
        if(this.readyState == 4 && this.status == 201){
            alert('Tweet Success')
            document.location='timeline.html'

            masukanTweet = JSON.parse(this.response);
            console.log(masukanTweet);

            document.getElementById('tweetscontainer').insertAdjacentHTML("afterbegin", `<div class="tweeting">    
            <div class="data-tweet">
                <img src="IMG/IMG_1526.JPG">
                <strong>${masukanTweet.email}</strong> <span>${masukanTweet.email} . 45m</span>
                <p>${masukanTweet.tweet}</p>

                <div class="btn-tweet">
                    <a href=""><i class="fa fa-comment"></i></a>
                    <a href=""><i class="fas fa-retweet"></i></a>
                    <a href=""><i class="fa fa-heart"></i></a>
                    <a href=""><i class="fab fa-gitter"></i></a>
                </div>
            </div>
        </div>`);
        }

        else if(this.readyState == 4){
            alert("Tweet gagal ditambhkan dengan error code: "+this.status);
        }
    };
}

function allTweet(){
    username = localStorage.getItem('username')

    var xmlHttp = new XMLHttpRequest();
    // xmlHttp.open("GET", "http://localhost:7000/api/v1/tweet");
    xmlHttp.open("POST", "http://localhost:5000/Tweet");
    xmlHttp.setRequestHeader("Content-Type", "application/json");
    xmlHttp.send(JSON.stringify({
        'username' : localStorage.getItem('username')
    }));
    xmlHttp.onreadystatechange = function() {
        if(this.readyState == 4 && this.status == 200) {
            jmlTweet = 0;

            JSON.parse(this.response).forEach(function (data, index) {
                if (username == data.username){
                    jmlTweet += 1;
                    document.getElementById("statslistitemcount").innerText = jmlTweet
                }
                document.getElementById('tweetscontainer').insertAdjacentHTML("afterbegin",`<div class="tweet" style="
                display: flex;
                align-items: center;
            ">
            <div class="images" style="
            margin-right: 1rem">
                <img src="${data.photoprofile}" alt="foto orang" style="
                width: 50px;
                height: 50px;
                border-radius: 50px"/>
            </div>
            <div class="content">
                <div class="fullname">
                    <b>${data.fullname}</b> <span>@${data.username}</span>
                </div>
                <div class="tweet">
                    <p>${data.content}</p>
                </div>
            </div>
            <div>
                <button type="submit" onclick="deleteTweet(this)" class="delete" id="del$(i)">Delete</button>
            </div>
        </div>`);
            });
        }
    }
}

// function allprofile(){

//     id = localStorage.getItem('id');

//     var xmlHttp = new XMLHttpRequest();
//     xmlHttp.open("POST","http://localhost:5000/")
// }

function deleteTweet(data){
    parent = document.getElementById(data.id).closest(".tweet");
    tweet = parent.querySelectorAll('p')[0].innerText;
    email = parent.querySelectorAll('h3')[0].innerText;
    date = parent.querySelectorAll('span')[0].innerText;

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("DELETE", "http://localhost:5000/AllTweet");
    xmlHttp.setRequestHeader("Content-Type", "application/json");
    xmlHttp.send(JSON.stringify({
        "email": email,
        "tweet": tweet,
        "date": date
    }));
}

function logout(){
    localStorage.clear();
    document.location='login.html'
}
function cekAuth(){
    var email = getCookie("email");
    if (email != "") {
        alert("Welcome again " + email);
    } else {
        email = prompt("Please enter your email:", "");
        if (email != "" && email != null) {
            setCookie("email", email, 365);
        }
    }
}
    // token = localStorage.getItem('email');
    // var 'email' = document.cookie;
    // alert(token)

//     if (token == null){
//         alert('Silakan login dahulu!')
//         localStorage.clear();
//         document.location='login.html'
//     }
// }
