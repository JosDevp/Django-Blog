var myFirebaseRef;
var chart;
var chartData=[];

$(document).ready(function(){
   myFirebaseRef =new Firebase("https://datalenguaje.firebaseio.com/");
   requestData();

})

requestData=function(){
	myFirebaseRef.on("value",function(data){
		var comidas=data.val();
		console.log(comidas);
	})
}


