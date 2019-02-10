// vars

var prev = document.getElementById("prev");
var next = document.getElementById("next");
var get_type = JSON.parse(document.getElementById("get-type").innerText);
var set_type = document.getElementById("search-type");
var offset_data = JSON.parse(document.getElementById("offset-data").innerText);

console.log(get_type);
console.log(set_type.value);

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
    next.style.display = "inline";
}

for (var i, j = 0; i = set_type.options[j]; j++){
	if(i.value == get_type.type){
		set_type.selectedIndex = j;
		break;
	}
}

// document.getElementById("showcase").removeChild(document.getElementById("offset-data"));

