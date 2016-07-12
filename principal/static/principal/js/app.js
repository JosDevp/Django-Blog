var myFirebaseRef;
var chart; // referencia de nuestra grafica
var chartData=[];

// var chartData=[
//  ['tacos',20],
//  ['paella',15],
//  ['ceviche',40],
//  ['mangu',50],


// ];

var flag= false;
var myTimer;

$(document).ready(function(){
   myFirebaseRef =new Firebase("https://datalenguaje.firebaseio.com/");
   $('#ceviche,#paella,#mangu,#tacos').click(vote);
   $("#bar,#pie,#donut").click(transformChart);
   $("#random").click(toggleRandom);
   requestData();
   addChart();

})

toggleRandom = function() {
    if (flag) {
        clearInterval(myTimer);
        flag = false;
        return;
    }

    myTimer = setInterval(randomVote, 100);
    flag = true;
}

randomVote = function() {
    var comidas = ['tacos', 'paella', 'ceviche', 'mangu'];
    var randomNumber = Math.floor(Math.random() * 4);
    var choosenOne = comidas[randomNumber];
    var voteCount = Number($("#votos_" + choosenOne + " span").text());

    myFirebaseRef.child(choosenOne).update({
        "votos": ++voteCount +randomNumber
    }, function() {
        console.log('Se realizó un voto por ' + choosenOne);
    })
}


transformChart=function(){

	chart.transform(this.id);

}

vote= function(){
	var choice=this.id;
	var voteCount=$("#votos_"+choice+" span").text();
	var self=this.id;
	console.log(voteCount);

	 $("#spinner").addClass('fa-refresh');
    
    $("#"  +  choice).prop("disabled", true);

	myFirebaseRef.child(choice).update({
    "votos":++voteCount


	},function(){
	   $("#" +  self).prop("disabled", false);
      console.log(' se realizo un voto por ' + self);
       $("#spinner").removeClass('fa-refresh');
	})
}

requestData=function(){
    var total;

    $("#spinner").addClass('fa-refresh');

	myFirebaseRef.on("value",function(data){
		total=0;
        chartData=[];

		var comidas=data.val();
		var arr;
		for(comida in comidas){
		    //console.log(comida,comidas[comida].votos,comidas[comida]);
            $("#votos_"+comida + " span").text(comidas[comida].votos);
            arr = [comida,comidas[comida].votos]
            chartData.push(arr)

            total += Number(comidas[comida].votos);


		}
		$("#total span").html(total);

		//chart.load({
		  chart.flow({
         columns:chartData
		});

		 $("#spinner").removeClass('fa-refresh');

		
	})
}


addChart=function(){

	chart= c3.generate({
		bindto:"#chart",
		data:{
			type:'bar',
		columns:chartData,
		colors:{

			    tacos: '#265a88',
                paella: '#419641',
                ceviche: '#2aabd2',
                mangu: '#eb9316'
		},
		names: {
                tacos: 'Tacos al pastor',
                paella: 'Paella Valenciana',
                ceviche: 'Ceviche Peruano',
                mangu: 'Mangú'
            }

		},
		 bar: {
            width: {
                ratio: 1
            }
        },
        tooltip: {
            format: {
                title: function(x) {
                    return 'Estado de votación';
                }
            }
        },
        axis: {
            rotated: false,
            y: {
                label: 'Cantidad de votos'
            },
            x: {
                show: true,
                label: 'Comidas'
            }
        },
        donut: {
            title: "La comida favorita"
        }
		
	})
}