function setup() {
    var header = document.getElementsByTagName("header")[0];

    var hamburger = document.createElement("button");
    hamburger.id = "hamburger";
    hamburger.classList.add("hamburger", "hamburger--spin");
    hamburger.type = "button";
    var hamburgerBox = document.createElement("span");
    hamburgerBox.classList.add("hamburger-box");
    var hamburgerInner = document.createElement("span")
    hamburgerInner.classList.add("hamburger-inner");
    hamburgerBox.append(hamburgerInner);
    hamburger.append(hamburgerBox);
    var imgURL = document.createElement("a");
    imgURL.href = "#";
    var img = document.createElement("img");
    img.src = "https://de-professionals.nl/wp-content/uploads/2017/10/logo-dummy.png"; // Give url
    img.alt = "Discord Marketplace Icon";
    imgURL.append(img);
    header.append(hamburger);
    header.append(imgURL);

    var nav = document.createElement("nav");
    var pre = document.createElement("div");
    pre.id = "pre";
    var preUL = document.createElement("ul");
    addLI(preUL, "Bots", "bots");  // Give url
    addLI(preUL, "Ads", "#");      // Give url
    addLI(preUL, "Servers", "#");  // Give url
    var sub = document.createElement("div");
    sub.id = "sub";
    var subUL = document.createElement("ul");
    addLI(subUL, "Home", "#");          // Give url
    addLI(subUL, "API", "#");           // Give url
    addLI(subUL, "Join Discord", "#");  // Give url
    addLI(subUL, "Login", "#");         // Give url
    pre.append(preUL);
    sub.append(subUL);
    nav.append(pre);
    nav.append(sub);
    header.append(nav);
}

function addLI(list, name, url) {
    var li = document.createElement("li");
    var a = document.createElement("a");
    a.innerHTML = name;
    a.href = url;
    li.append(a);
    list.append(li);
    
}

setup();

$("#hamburger").click(function () {
    $(this).toggleClass("is-active");
    $('header').toggleClass('active');
})