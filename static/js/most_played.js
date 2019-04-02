// variables
var search_bar_most_played = document.getElementById("most-played-form");
var footer = document.getElementById("footer");
var modal = document.getElementById("make-playlist-modal");
var short_modal_button = document.getElementsByClassName("make-playlist")[0];
var medium_modal_button = document.getElementsByClassName("make-playlist")[1];
var long_modal_button = document.getElementsByClassName("make-playlist")[2];
var close_modal_button = document.getElementsByClassName("close-btn")[0];
var close_form_button = document.getElementsByClassName("close-btn")[1];

// eventListeners
search_bar_most_played.addEventListener("submit", filterList);
short_modal_button.addEventListener("click", open_modal);
medium_modal_button.addEventListener("click", open_modal);
long_modal_button.addEventListener("click", open_modal);
close_modal_button.addEventListener("click", close_modal);
close_form_button.addEventListener("click", close_modal);
window.addEventListener("click", click_outside);
// functions
function filterList(e){
    var type = document.querySelector("#showcase #most-played-form #type").value;
    var term = document.querySelector("#showcase #most-played-form #term").value;
    e.preventDefault();
    if(((type == null || type == "") && (term == null || term == "")) || ((type != null || type != "") && (term == null || term == "")) || (type == null || type == "") && (term != null || term != "")){
        alert("Please fill values!");      
    }

    else if(type == "artist"){
        if (term == "short_term") {
            document.getElementById("short-term").style.display = "block";
            document.getElementById("short-term-tracks").style.display = "none";
            document.getElementById("short-term-artists").style.display = "block";
            document.getElementById("medium-term").style.display = "none";
            document.getElementById("long-term").style.display = "none";
            footer.style.display = "block";
            footer.style.position = "relative";
            short_modal_button.style.display = "none";
        } else if(term == "medium_term") {
            document.getElementById("short-term").style.display = "none";
            document.getElementById("medium-term").style.display = "block";
            document.getElementById("medium-term-tracks").style.display = "none";
            document.getElementById("medium-term-artists").style.display = "block";
            document.getElementById("long-term").style.display = "none";
            footer.style.display = "block";
            footer.style.position = "relative";
            medium_modal_button.style.display = "none";
        } else if (term == "long_term") {
            document.getElementById("short-term").style.display = "none";
            document.getElementById("medium-term").style.display = "none";
            document.getElementById("long-term").style.display = "block";
            document.getElementById("long-term-tracks").style.display = "none";
            document.getElementById("long-term-artists").style.display = "block";
            footer.style.display = "block";
            footer.style.position = "relative";
            long_modal_button.style.display = "none";
        }
    } 
    else if (type == "track"){
        if (term == "short_term") {
            document.getElementById("short-term").style.display = "block";
            document.getElementById("short-term-tracks").style.display = "block";
            document.getElementById("short-term-artists").style.display = "none";
            document.getElementById("medium-term").style.display = "none";
            document.getElementById("long-term").style.display = "none";
            footer.style.display = "block";
            footer.style.position = "relative";
            short_modal_button.style.display = "block";
        } else if (term == "medium_term"){
            document.getElementById("short-term").style.display = "none";
            document.getElementById("medium-term").style.display = "block";
            document.getElementById("medium-term-tracks").style.display = "block";
            document.getElementById("medium-term-artists").style.display = "none";
            document.getElementById("long-term").style.display = "none";
            footer.style.display = "block";
            footer.style.position = "relative";
            medium_modal_button.style.display = "block";
        } else if (term == "long_term") {
            document.getElementById("short-term").style.display = "none";
            document.getElementById("medium-term").style.display = "none";
            document.getElementById("long-term").style.display = "block";
            document.getElementById("long-term-tracks").style.display = "block";
            document.getElementById("long-term-artists").style.display = "none";
            footer.style.display = "block";
            footer.style.position = "relative";
            long_modal_button.style.display = "block";
        }
    }
}

function open_modal(){
    modal.style.display = "block";
}

function close_modal(){
    modal.style.display = "none";
    window.location.href = "#";
}

function click_outside(e){
    if(e.target == modal){
        modal.style.display = "none";
        window.location.href = "#";
    }
}