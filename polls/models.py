from django.db import models
        
class Game(models.Model):
	complete = models.BooleanField(default=False)
	square_0 = models.IntegerField(max_length=1,default=0)
	square_1 = models.IntegerField(max_length=1,default=0)
	square_2 = models.IntegerField(max_length=1,default=0)
	square_3 = models.IntegerField(max_length=1,default=0)
	square_4 = models.IntegerField(max_length=1,default=0)
	square_5 = models.IntegerField(max_length=1,default=0)
	square_6 = models.IntegerField(max_length=1,default=0)
	square_7 = models.IntegerField(max_length=1,default=0)
	square_8 = models.IntegerField(max_length=1,default=0)
	turn = models.IntegerField(max_length=1,default=1)
	difficulty = models.IntegerField(max_length=1,default=0)
	
	def addSquare(self,n):
		#make sure the game is not done
		if self.complete == True:
			return False			
		test = getattr(self,'square_'+str(n))
		if test == 0:
			#square is empty, valid move!
			setattr(self,'square_'+str(n),self.turn)
			self.turn = 1 if self.turn == 2 else 2
			#Check to see if the last move filled the board
			if not self.hasEmpty():
				self.complete = True
				self.turn = 0	
			self.save()			
			return True
		else:
			return False
			
	def gameWin(self,p):
		#check to see if the game is won by player p		
		for path in self.buildPaths():
			if path.count(p) == 3:
				self.complete = True
				return True			
		return False
		
	def buildPaths(self):
		#build a list of all squares
		s = []
		for x in range(9):
			s.append(getattr(self,'square_'+str(x)))
		
		#there are 8 possible winning paths (3 horizontal, 3 vertical, and 2 diagonals
				
		paths = [ [s[0],s[1],s[2]], [ s[3],s[4],s[5]], [ s[6],s[7],s[8]],	#horizontals
		[s[0],s[3],s[6]], [ s[1],s[4],s[7]], [ s[2],s[5],s[8]],				#verticals
		[s[0],s[4],s[8]],[s[6],s[4],s[2]]]									#diagonals
	
		return paths
		
	def dumbAI(self):
		from random import choice
		#easyAI will just mark a random empty square
		
		s = []
		for x in range(9):
			if getattr(self,'square_'+str(x)) == 0:		
				s.append(x)
		return choice(s)
		
	
	def smartAI(self):
		from random import choice
		#smartAI will look for winning paths and block you
		paths = self.buildPaths()
		
		#first we will check for paths that we have marked twice (2) and the third is empty (0)
		i = 0
		for path in paths:
			if path.count(2) == 2 and path.count(0) == 1:
				#this is a winning path
				return self.pathToSquare(i,paths)
			i += 1
		#didn't find any winning paths... block any oppoent winning paths
		i = 0
		for path in paths:
			if path.count(1) == 2 and path.count(0) == 1:
				#this is a winning path - stop them!
				return self.pathToSquare(i,paths)
			i += 1
		#there weren't any paths to block... fill in any empty square!
		s = []
		for x in range(9):
			if getattr(self,'square_'+str(x)) == 0:		
				s.append(x)				
		return choice(s)
	
	def hasEmpty(self):
		#determines if there is an empty square (and the game shall continue)
		s = []
		for x in range(9):
			if getattr(self,'square_'+str(x)) == 0:
				return True
		return False
		
	def pathToSquare(self,i,paths):
		#this is a bit hacky, but will help translate a path into it's empty square
		#	Squares					Paths
		#	0	1	2				0,1,2 horitzontals
		#	3	4	5				3,4,5 verticals		
		#	6	7	8				6,7   diagonals
		
		#e.g., path 0 is squares 0,1,2

		#translate path to squares	
		#horizontals
		if i == 0:
			return self.returnEmptySquare(paths[i],range(0,3))
		elif i == 1:
			return self.returnEmptySquare(paths[i],range(3,6))
		elif i == 2:
			return self.returnEmptySquare(paths[i],range(6,9))
		#verticals
		elif i == 3:
			return self.returnEmptySquare(paths[i],[0,3,6])		
		elif i == 4:
			return self.returnEmptySquare(paths[i],[1,4,7])
		elif i == 5:
			return self.returnEmptySquare(paths[i],[2,5,8])
		#diagonals
		elif i == 6:
			return self.returnEmptySquare(paths[i],[0,4,8])
		elif i == 7:
			return self.returnEmptySquare(paths[i],[6,4,2])
		else:
			return False
								
	def returnEmptySquare(self,path,squares):
		#this scans the path for the empty square
		i = 0
		for j in squares:
			if path[i] == 0:
				return j
			i += 1
		return False
		
	def first(self):
		#determines who goes first
		from random import choice
		turn = choice(range(1,3))
		
		if turn == 2:
			#computer goes first!
			self.turn = 2
			if self.difficulty == 0:
				move = choice(range(9))
			else:
				move = 4	#smartAI will always start in the center
			self.addSquare(move)
			return move
		return False
		
	def setDifficulty(self,ai):
		if ai == '1':
			self.difficulty = 1
		else:
			self.difficulty = 0		
		self.save()