(function(){
    "use strict";

    let navButtons = document.getElementsByClassName("nav-link");
    for (let i in navButtons) {
        if (navButtons.hasOwnProperty(i)) {
            let classes = navButtons[i].className || "";
            let loc = window.location.pathname || "";

            if (loc == "/admin" && classes.indexOf("admin") !== -1) {
                navButtons[i].className += " active";
            }
            
            if (loc == "/" && classes.indexOf("basic") !== -1) {
                navButtons[i].className += " active";
            }
            
            if (loc == "/admin/advanced" && classes.indexOf("advanced") !== -1) {
                navButtons[i].className += " active";
            }
        }
    }

    
})();