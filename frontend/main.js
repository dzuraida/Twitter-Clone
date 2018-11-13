function klik() {
  alert("alohamora beybeh");
}

function signUp() {
  // debugger
  username = document.getElementById("username").value;
  email = document.getElementById("email").value;
  fullname = document.getElementById("full-name").value;
  password = document.getElementById("password").value;

  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open("POST", "http://localhost:5000/signup");
  xmlHttp.setRequestHeader("Content-Type", "application/json");
  xmlHttp.send(
    JSON.stringify({
      username: username,
      email: email,
      password: password,
      fullname: fullname
    })
  );
  xmlHttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 201) {
      alert("Data Berhasil Di Submit dengan Status Code: " + this.status);
      window.location = "/login.html";
    } else if (this.readyState == 4) {
      alert("Data gagal di input: " + this.status);
    }
  };
}

function signIn() {
  // debugger
  email = document.getElementById("email").value;
  password = document.getElementById("password").value;

  var xmlRequest = new XMLHttpRequest();
  xmlRequest.open("POST", "http://localhost:5000/login");
  xmlRequest.setRequestHeader("Content-Type", "application/json");
  xmlRequest.send(
    JSON.stringify({
      email: email,
      password: password
    })
  );
  xmlRequest.onreadystatechange = function() {
    // alert(this.response)
    if (this.readyState == 4 && this.status == 200) {
      // alert(this.response)
      // localStorage.setItem('email', this.response);
      // localStorage.setItem('username', this.response);
      // localStorage.setItem('password', this.response);
      document.cookie = "email=" + this.response;
      window.location = "/timeline.html";
    } else if (this.readyState == 4) {
      alert("SignIn gagal dengan status code :" + this.status);
    }
  };
}

function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(";");
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == " ") {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function getProfile() {
  // username = localStorage.getItem('username')
  // alert(username)
  var xmlProfile = new XMLHttpRequest();
  xmlProfile.open("POST", "http://localhost:5000/getProfile");
  // xmlProfile.setRequestHeader("Content-Type","application/json");
  xmlProfile.setRequestHeader("Authorization", getCookie("email"));
  xmlProfile.send();
  // xmlProfile.send(JSON.stringify({
  //     "username":username
  // }));
  xmlProfile.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      profile = JSON.parse(this.response);
      // alert(this.response)
      document.getElementById("profile-fullname").innerText = profile.fullname;
      document.getElementById("profile-foto").src = profile.photoprofile;
      document.getElementById("nav-pic").src = profile.photoprofile;
      document.getElementById("tweet-pic").src = profile.photoprofile;
      // document.getElementById("user-name").innerText = (profile.username)
      // document.getElementById("bio").innerText = (profile.bio)
    }
  };
}

function addTweet() {
  var xmlHttp = new XMLHttpRequest();
  tweet = document.getElementById("posttweetta").value;
  xmlHttp.open("POST", "http://localhost:5000/tweeting");
  xmlHttp.setRequestHeader("Content-Type", "application/json");
  xmlHttp.setRequestHeader("Authorization", getCookie("email"));
  xmlHttp.send(
    JSON.stringify({
      tweet: tweet
    })
  );
  xmlHttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 201) {
      alert("Tweet Success");
      document.location = "timeline.html";

      masukanTweet = JSON.parse(this.response);
      console.log(masukanTweet);

      document.getElementById("tweetscontainer").insertAdjacentHTML(
        "afterbegin",
        `<div class="tweeting">    
            <div class="data-tweet">
                <img src="IMG/2.jpg">
                <strong>${masukanTweet.email}</strong> <span${
          masukanTweet.email
        } </span>
                <p>${masukanTweet.tweet}</p>

            </div>
        </div>`
      );
    } else if (this.readyState == 4) {
      alert("Tweet gagal ditambhkan dengan error code: " + this.status);
    }
  };
}

function allTweet() {
  // username = localStorage.getItem('username')
  // alert('ada')

  var xmlHttp = new XMLHttpRequest();
  // xmlHttp.open("GET", "http://localhost:7000/api/v1/tweet");
  xmlHttp.open("GET", "http://localhost:5000/Tweet");
  xmlHttp.setRequestHeader("Content-Type", "application/json");
  xmlHttp.setRequestHeader("Authorization", getCookie("email"));
  xmlHttp.onreadystatechange = function() {
    // alert(this.response)
    if (this.readyState == 4 && this.status == 200) {
      // jmlTweet = 0;
      JSON.parse(this.response).forEach(function(data, index) {
        var tweets = JSON.parse(data.tweets);
        tweets.forEach(function(tweet, idx) {
          document.getElementById("tweetscontainer").insertAdjacentHTML(
            "afterbegin",
            `<div class="tweet" id=${tweet.id} style="
                    display: flex;
                    align-items: center;
                    grid-template-columns: 1fr 3fr 1fr;
                    grid-template-areas:
                    "picture name button"
                    "picture tweet date";
                    justify-content: space-between;
                ">
                <div class="images" style="
                margin-right: 1rem;
                grid-area: picture">
                    <img src="${data.photoprofile}" alt="foto orang" style="
                    width: 50px;
                    height: 50px;
                    border-radius: 50px"/>
                </div>
                <div class="content">
                    <div class="fullname" style="grid-area: name">
                        <b>${data.fullname}</b> <span>@${data.username}</span>
                    </div>
                    <div class="tweet" style="grid-area: tweet">
                        <p>${tweet.content}</p>
                    </div>
                </div>
                <div class="button">
                    <div class="delete" style="grid-area: button">
                    <button type="submit" id="delete-tweet" onclick="deleteTweet(${
                      tweet.id
                    })">Delete</button>
                    </div>
                    <div class="date" style="grid-area: date">
                    <p>${tweet.date}</p>
                    </div>
                </div>
            </div>`
          );
        });
        // if (email == data.email) {
        // jmlTweet += 1;
        // document.getElementById("statslistitemcount").innerText = jmlTweet
        // }
      });
    }
  };
  xmlHttp.send();
}

// function allprofile(){

//     id = localStorage.getItem('id');

//     var xmlHttp = new XMLHttpRequest();
//     xmlHttp.open("POST","http://localhost:5000/")
// }

function deleteTweet(id) {
  // parent = document.getElementById(data.id).closest(".tweet");
  // tweet = parent.querySelectorAll('p')[0].innerText;
  // email = parent.querySelectorAll('h3')[0].innerText;
  // date = parent.querySelectorAll('span')[0].innerText;

  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open("DELETE", "http://localhost:5000/deletetweet");
  xmlHttp.setRequestHeader("Content-Type", "application/json");
  xmlHttp.setRequestHeader("Authorization", getCookie("email"));
  var deleted = {
    id: id
  };
  xmlHttp.send(JSON.stringify(deleted));
  xmlHttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var tweet = document.getElementById(id)
      tweet.remove()
    }
  };
}

function logout() {
  var mydate = new Date();
  mydate.setTime(mydate.getTime() - 1);
  document.cookie = "email=; expires=" + mydate.toGMTString();
  document.location = "login.html";
}

function cekAuth() {
  var email = getCookie("email");
  if (email != "") {
    // alert("Welcome again " + email);
  } else {
    alert("Please Login");
    var mydate = new Date();
    mydate.setTime(mydate.getTime() - 1);
    document.cookie = "email=; expires=" + mydate.toGMTString();
    document.location = "login.html";
    // email = prompt("Please enter your email:", "");
    // if (email != "" && email != null) {
    //     setCookie("email", email, 365);
    // }
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
