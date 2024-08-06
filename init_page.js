document.addEventListener("DOMContentLoaded", () => {
    var art = document.querySelector("#art");
    art.addEventListener("load", () => {
        var initialWindowWidth = window.innerWidth;
        var initialWindowHeight = window.innerHeight;
        if(art.naturalWidth > art.naturalHeight) {
            art.width=initialWindowWidth*.70;
        } else {
            art.height=initialWindowHeight*.70;
        }
    });
});
