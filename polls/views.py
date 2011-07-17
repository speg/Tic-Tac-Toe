# Create your views here.
from myproject.polls.models import Game
from django.shortcuts import render_to_response,get_object_or_404
from django.http import HttpResponse

def index(request):
    return render_to_response('polls/index.html')
     
def action(request):
	#browser requests to do something
	
	action = request.GET['action']	
	result = False
	AImove = 'null'
	victory = 'none'
	#set up return variables
		
	#python doesn't have native switch? who knew!
	if action == 'add':
		#fetch the current game
		game = Game.objects.get(pk=request.GET['id'])
		square = request.GET['square']
		result = game.addSquare(square)
		
		if result:
			win = game.gameWin(1)	#did you win?
			
			if win:				
				victory = 'Win'
			elif not game.complete:
				#make AI move
				if game.difficulty == 0:
					AImove = game.dumbAI()
				else:
					AImove = game.smartAI()
				game.addSquare(AImove)
				#check if AI won
				if game.gameWin(2):
					victory = 'Lose'					
				elif game.complete:
					victory = 'Draw'			
			else:
				#draw game
				victory = 'Draw'
			game.save()	
		
		result = '{"id":"'+ request.GET['id']+'","result":'+str(result).lower() +',"turn":'+str(game.turn)+',"victory":"'+victory+'","AImove":'+str(AImove)+'}'
	
	elif action == 'new':
		#create a new game
		new = Game()
		new.setDifficulty(request.GET['ai'])
		first = new.first()
		new.save()
		result = '{"id":'+ str(new.id)+',"first":'+str(first).lower()+'}'
		
	elif action == 'ai':
		#change difficulty
		game = Game.objects.get(pk=request.GET['id'])
		game.setDifficulty(request.GET['smarts'])
		result = '{"ai":'+str(game.difficulty)+', "id":'+ str(game.id)+'}'	
	
	return HttpResponse(result)