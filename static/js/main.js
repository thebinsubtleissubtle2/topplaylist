// TODO: validations on searching
// TODO: Show tables through filters.

// variables
var search_bar_index = document.querySelector("#showcase #landing form");


// events
search_bar_index.addEventListener("submit", submitLanding);


function submitLanding(e){
	var get_value = document.querySelector("#showcase #landing input[type = \"text\"]").value;
	if(get_value == null || get_value == ""){
		alert("Please fill values.");
		e.preventDefault();
	}
}