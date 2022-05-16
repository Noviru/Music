function loadDoc(zoneList) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
	var dict = this.response;
	var jsonDict = JSON.parse(dict);
	if(jsonDict["error"] != ''){
	document.getElementById("error").innerHTML =jsonDict["error"];
}
	else{
	document.getElementById("error").innerHTML = "No error :)";
}
    }
  };
  xhttp.open("GET", "/nextState", true);
  xhttp.send();
}

function nextStates(zoneList){
  var jsonData = {process: zoneList[0],state: zoneList[1],name: zoneList[2],error: zoneList[3]};
  $.ajax({
  type: "POST",
  url: "/nextState",
  data: JSON.stringify(jsonData),
  contentType: "application/json",
  dataType: 'json',
  success: function(result) {
    console.log("Result:");
    //Document id for dnskeysynce
    var process = result["process"];
    var zoneName = result["name"];
    var state = result["state"];
    const element = document.getElementById(state + "_" + zoneName+"_"+process);
    document.getElementById(zoneName+"_process").innerHTML = result["process"];
    console.log(zoneName+"_"+process);
    document.getElementById(zoneName+"_"+process).style.backgroundColor = "#00FF00";
    console.log(result);
  }
});
}


function removeSigner(zoneList) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
	console.log("tja");
    }
  };
  xhttp.open("GET", "/removeSigner", true);
  xhttp.send(zoneList);
}


