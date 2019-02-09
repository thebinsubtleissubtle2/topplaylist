var search_bar_most_played = document.getElementById("most-played-form");

search_bar_most_played.addEventListener("submit", filterList);
/* TODO: make animations on filterList */
function filterList(e){
    var type = document.querySelector("#showcase #most-played-form #type").value;
    var term = document.querySelector("#showcase #most-played-form #term").value;
    e.preventDefault();
    if(((type == null || type == "") && (term == null || term == "")) || ((type != null || type != "") && (term == null || term == "")) || (type == null || type == "") && (term != null || term != "")){
        alert("Please fill values!");      
    }

    else if (type == "track" && term == "short-term"){
        document.getElementById("short-term").style.display = "block";
        document.getElementById("short-term-tracks").style.display = "block";
        document.getElementById("short-term-artists").style.display = "none";
        document.getElementById("medium-term").style.display = "none";
        document.getElementById("long-term").style.display = "none";
    }

    else if (type == "artist" && term == "short-term"){
        document.getElementById("short-term").style.display = "block";
        document.getElementById("short-term-tracks").style.display = "none";
        document.getElementById("short-term-artists").style.display = "block";
        document.getElementById("medium-term").style.display = "none";
        document.getElementById("long-term").style.display = "none";
    }

    else if (type == "track" && term == "medium-term"){
        document.getElementById("short-term").style.display = "none";
        document.getElementById("medium-term").style.display = "block";
        document.getElementById("medium-term-tracks").style.display = "block";
        document.getElementById("medium-term-artists").style.display = "none";
        document.getElementById("long-term").style.display = "none";
    }

    else if (type == "artist" && term == "medium-term"){
        document.getElementById("short-term").style.display = "none";
        document.getElementById("medium-term").style.display = "block";
        document.getElementById("medium-term-tracks").style.display = "none";
        document.getElementById("medium-term-artists").style.display = "block";
        document.getElementById("long-term").style.display = "none";
    }

    else if (type == "track" && term == "long-term"){
        document.getElementById("short-term").style.display = "none";
        document.getElementById("medium-term").style.display = "none";
        document.getElementById("long-term").style.display = "block";
        document.getElementById("long-term-tracks").style.display = "block";
        document.getElementById("long-term-artists").style.display = "none";
    }
    
    else if (type == "artist" && term == "long-term"){
        document.getElementById("short-term").style.display = "none";
        document.getElementById("medium-term").style.display = "none";
        document.getElementById("long-term").style.display = "block";
        document.getElementById("long-term-tracks").style.display = "none";
        document.getElementById("long-term-artists").style.display = "block";
    }
}