var prev = document.getElementById("prev");
var next = document.getElementById("next");

var offset_data = JSON.parse(document.getElementById("offset-data").innerText);

if(offset_data.prev_offset < 0){
    prev.style.display = "none";
    // prev.addEventListener("click", function(e){
    //     if(e.target.)
    // });
}
else{
    prev.style.display = "inline";
}
if(offset_data.next_offset > offset_data.total){
    next.style.display = "none";
}
else{
    next.style.display = "none";
}