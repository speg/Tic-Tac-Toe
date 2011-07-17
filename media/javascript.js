function drawSquare(n,p){
	var x = 'X'
	var url = 'url(/media/images/python.png)';
	if(p == 2){x = 'O';url = 'url(/media/images/lion.png)';}	
	if(MY_SETTINGS.graphicsON){$('#b'+n).css('background-image',url);}
	else{$('#b'+n).html(x);}	
}

function newGame(){
	
	$('.box').html('').css('background-image','');
	$('#victory').fadeOut('fast');
	
	$.getJSON('http://speg.webfactional.com/action/?action=new&ai='+MY_SETTINGS.difficulty , function(data){
		$("#debug").html('New game# '+data.id+' started\n\nfirst move:'+data.first);
		MY_SETTINGS.gameID = data.id;
		if(data.first === false){
			//do nothing, wait for player to play
		}else{
			//computer made the first move, place it on the board
			drawSquare(data.first,2);
		}
	});
}

$(document).ready(function() {
	
	//bind listener to new game button
	$('#new').bind('click',function(){
		//reset to a new game
		newGame();		    
	});
  
	//bind graphics on/off button
	$('#graphics').bind('click',function(){
  	//toggle graphics on/off
  	MY_SETTINGS.graphicsON = !MY_SETTINGS.graphicsON
  	
  	if(MY_SETTINGS.graphicsON){
  		$('#graphics').html('Graphics On');
  		$('.box').each(function(){
  			//te = $(this).html();
  			if($(this).html() == 'X'){
  				$(this).css('background-image','url(/media/images/python.png)');
  			}else if ($(this).html() == 'O'){
  				$(this).css('background-image','url(/media/images/lion.png)');
  			}
  			$(this).html('');
  		});
  		}else{
  			$('#graphics').html('Graphics Off');
	  		$('.box').each(function(){
	  			
	  			if($(this).css('background-image') == 'url(http://speg.webfactional.com/media/images/python.png)'){
	  				$(this).html('X');
	  			}else if ($(this).css('background-image') == 'url(http://speg.webfactional.com/media/images/lion.png)'){
	  				$(this).html('O');
	  			}
				$(this).css('background-image','');
	  		});
  		}
	});
  
	//attach difficulty button handler and function
	$('#ai').bind('click',function(){
		if(MY_SETTINGS.difficulty == 0){
			MY_SETTINGS.difficulty = 1;
			$(this).html('Hard');
		}else{
			MY_SETTINGS.difficulty = 0;
			$(this).html('Easy');
		}
		
		var li = 'http://speg.webfactional.com/action/?action=ai&id='+MY_SETTINGS.gameID+'&smarts='+MY_SETTINGS.difficulty;
  		
  		$.getJSON(li,function(data){
  			$('#debug').html(data.ai+' MY_SETTINGS. difficulty: '+MY_SETTINGS.difficulty+' '+data.id);
  		});	  
	});

  //attach handlers to the squares		  
  $('.box').bind('click',function(){
	  	
	  	var square = this.id.substring(1);
	  	var link = 'http://speg.webfactional.com/action/?action=add&square='+square+'&id='+MY_SETTINGS.gameID;
  
  		$.getJSON(link , function(data){
  			$("#debug").html(data.result+', turn'+data.turn+', AImove: '+data.AImove+', finished: '+data.victory);
  			if(data.result){
				drawSquare(square,1);
				if(data.AImove != null){										
					drawSquare(data.AImove,2);
				}  				
  				switch(data.victory){  				
  					case "Win":
  						//alert('Congratulations! You have achieved victory!');
  						$('#victory').css('background-position','0px 0px').html('Victory!').fadeIn(400);

  						break;
  					case 'Lose':
  						$('#victory').css('background-position','0px -210px').html('Defeat!').fadeIn(400);
						break;
  					case 'Draw':
  						$('#victory').css('background-position','0px -420px').html('Draw!').fadeIn(400);
  						break;
  					case "none":
  						//carry on
  						break;
  					default:
  						alert('Uh oh, this shouldn\'t have happened...');
  				}
  			}
  		});
  });  	
	//set up global settings and start a game
	MY_SETTINGS = { gameID : null, graphicsON : false, difficulty : 0};
	newGame();
});