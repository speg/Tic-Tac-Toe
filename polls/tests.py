from django.utils import unittest
from polls.models import Game

class myFirstTestCase(unittest.TestCase):
	def testBasic(self):
		a = 4
		b = 4
		self.assertEqual(a,b)

	def testmakeGame(self):		
		p = Game()
		self.assertEquals(p.turn,1)
		p.addSquare(1)
		self.assertEquals(p.turn,2)	#game has changed turn
		self.assertEquals(p.addSquare(1),False)	#insure you cannot add to an already used square
		
	def teststuff(self):
		p = Game()
		p.addSquare(0)
		p.addSquare(4)
		p.addSquare(1)
		p.addSquare(6)
		p.addSquare(2)
		self.assertEquals(p.gameWin(1),True)	#player wins
		self.assertEquals(p.addSquare(3),False)	#the game is over - you can't add more!
		
	def testAIgoesFirst(self):
		p = Game()
		p.difficulty = 1
		p.turn = 2	#set AI to go first
		first = p.first()
		if first is False:
			pass#player goes first
		else:
			self.assertEquals(p.square_4,2)	#ensure AI starts in the middle
		#random checks because i'm new to python
		self.assertEquals(False,0)
		g = 4
		h = 4
		if g is h:
			print 'it worked'
		else:
			print 'no dice'
	
	def testChangeDifficulty(self):
		p = Game()
		p.setDifficulty('1')	#input must be string because it's a GET parameter
		self.assertEquals(p.difficulty,1)
		
		
		
		
		
		