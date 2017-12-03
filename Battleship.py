from ships_classes import enemyShip, playerShip
from find_hidden_ships import *
from random import randint, seed
from copy import deepcopy
import sys , traceback

#----------------------------------global---------------------------


class Computer:
	def __init__(self):
		self.board = []  # field of the computer (where the player attacks)
		self.ships = []  # ships belonging to computer
		self.sunk = []  # computer ships that are sunk
		self.definition = [[ "Carrier" , 5] , [ "Battleship" , 4 ] , [ "Cruiser1" , 3] , [ "Cruiser2" , 3] , ["Frigate" , 2]]	#used to hold the ships to be created
		self.boardSize = 10
		self.alreadyAttacked = []
		self.previousHits = []  #testing

class Player:
	def __init__ (self):
		self.board = []  # field of the computer (where the player attacks)
		self.ships = []  # ships belonging to player
		self.sunk = []  # player ships that are sunk
		self.definition = [[ "Carrier" , 5] , [ "Battleship" , 4 ] , [ "Cruiser1" , 3] , [ "Cruiser2" , 3] , ["Frigate" , 2]]	#used to hold the ships to be created
		self.boardSize = 10
		self.alreadyAttacked = []
		self.previousHits = []  #testing


#————————————————create board————————————————#

def create_board(obj):         	#creates board
	for x in range(0, obj.boardSize):	#iterate through lists
		obj.board.append([])			#create lists in list
		obj.board[0].append(x)	#add counts to first row
		if x > 0:
			for i in range(0, obj.boardSize):		#iterate through list				
				obj.board[x].append("~")				#adds empty elements to lists in list
		obj.board[x][0] = x			#add row number as first element of board[1] and on	


def createPlayersBoard(obj):	
	for ship in obj.ships:		#change 0 to S for location of ship
		for i in ship.location:	#[[i], [i], [i]...]
			obj.board[i[0]][i[1]] = 'S'
	print_board(obj)


#-------------------------create enemy ships------------------------

def createEnemysShips(obj):					#create ships
	tempShips = list()
	for i in obj.definition:
		shipObject = enemyShip(i[0] , i[1], tempShips)
		obj.ships.append(shipObject)
		tempShips.append(shipObject)


#-------------------create player ships-----------------------------

def shipGenerationOption(obj):
	print("\n\nWelcome to Battleship!\n\
From here you have the option to have the computer randomly place your ships,\n\
or you may do it yourself")
	if input("Would you like the computer to place your ships? (Y/N): ").lower() == "y":
		generatePlayersShips(obj)
	else:
		print("You have chosen to place your ships")
		createPlayersShips(obj)
	print("\n")


"""computer generates player's boards"""
def generatePlayersShips(obj):
	create_board(obj)
	tempShips = list()
	for i in obj.definition:
		shipObject = enemyShip(i[0] , i[1], tempShips)
		obj.ships.append(shipObject)
		tempShips.append(shipObject)
	print("You have decided to autogenerate your ships")
	createPlayersBoard(obj)


def createPlayersShips(obj):
	tempShips = list()
	create_board(obj)
	print("Your ship will be on a" , (obj.boardSize-1), "x", (obj.boardSize-1), "board\n")
	print("From here you will place your ships. You enter the start point of the ship, from which \n\
a ship will be generated for the length of the ship either vertically or horizontally as chosen \nby you.")
	
	for info in obj.definition:
		orientation, startInput = getPlayerInput(obj.boardSize, info)
		shipObject = playerShip(info[0] , orientation , info[1] , startInput, tempShips)
		obj.ships.append(shipObject)
		tempShips.append(shipObject)
		
		createPlayersBoard(obj)	 # print board
		print(shipObject.name, "created at" , shipObject.location, "\n")
		print("---------------------------------------------\n")


def getPlayerInput(size, info):
	allowableSize = size - info[1] 
	while True:
		print("\nYour next ship is" , info[0] , ".  Please choose an orientation ('vertical', 'v' or 'horizontal', 'h')")
		orientation = input("Orientation: \t").lower()
		print("\n")
		if orientation == 'vertical' or orientation == 'v' or orientation == 'horizontal' or orientation == 'h':
			break
		print("Sorry, that is not a valid input.  Please try again\n")
	if orientation == "horizontal" or orientation == "h":
		print(info[0] , "has a size of" , info[1] , "Please enter a coordinate between [1-", size - 1 , ", 1-" , allowableSize , "]")
		orientation = 0
	else:
		print(info[0] , "has a size of" , info[1] , "Please enter a coordinate between [1-" , allowableSize , ", 1-" , size - 1 , "]")
		orientation = 1
	
	while True:
		startInput = list()
		try:
			startInput = [int(x) for x in input("Please enter a start coordinate\neg 4 , 3\nCoordinate:  \t").split(",")]
			if startInput[(orientation+1)%2] <= allowableSize and startInput[(orientation)%2] <= size - 1 and all(0 < startInput[i] for i in range(0,1))\
and len(startInput)==2:
				break
			else:
				print("That coordinate is incorrect.  Please try again\n")
		except:
			print("That is not a correct input. Please try again")
	return orientation, startInput
		

#-----------------------game play-----------------------------------
class Gameplay:
	def __init__(self):
		self.turn = randint(0,1)  # 1 for player's turn, 0 for computer's
		self.computerPlayForMe = False
		self.crossPattern = [[1,1], [2,2], [3,3], [4,4], [5,5], [6,6], [7,7], [8,8], [9,9], [1,9], [2,8], [3,7], [4,6], [6,4], [7,3], [8,2], [9,1]]	#list of initial attack points for cross pattern
		
		self.computerShouldPursue = []

		self.circling = False  # \\circling()
		self.process = 0  # \\circling()
		self.initialHit = []  # \\circling()
		
		self.firstHit = []
		self.previousHit = []
		self.targeting = False
		self.orientation = 0  # opposite of what it actually is (if h:1, if v:0).  Do not reset in targeting on
		self.nextTo = [-1, 1]  # attack L/R or U/D; once the attackPoint is a miss, nextTo.remove(int).  If empty, targeting = false, nextTo.reset

	# used to activate circling; circling not activated and targeting not activated
	def circlingOn(self, attackPoint):
		# if self.turn == 0 and self.targeting == False and self.circling == False:  
		self.circling = True
		self.initialHit = attackPoint
		self.process = 0

	def targetingOn(self, attackPoint):
		# print("targetingOn")  #testing
		self.targeting = True
		self.firstHit = self.initialHit
		self.previousHit = attackPoint
		self.circlingOff()

	def targetingOff(self):
		# print("targetingOff")  #testing
		self.nextTo = [-1, 1]
		self.targeting = False
		self.orientation = 0
		self.firstHit = []
		self.previousHit = []
		return self.nextTo, self.targeting, self.orientation, self.firstHit,  self.previousHit  

	def circlingOff(self):
		# print("circlingOff")  #testing
		self.circling = False  # \\circling()
		self.process = 0  # 
		self.initialHit = []  # \\circling()
		return self.circling, self.process, self. initialHit


"""# decide turn and display, take input/computer play, check if ship is dead"""
def isTurn(obj_comp, obj_player):	
	gameplay = Gameplay()
	while True:	 # continual gameplay
		if gameplay.turn:  # player's turn
			print("\n------------------------------------")
			if gameplay.computerPlayForMe:
				playForMe(gameplay, obj_comp)  # testing
			else:
				playersTurn(gameplay, obj_comp)
			checkGameIsWon(gameplay, obj_comp)
			print("\nEnemy field:")
			print_board(obj_comp)
			print("Your field:")
			print_board(obj_player)
			gameplay.turn = 0
			
		else:  # computer's turn
			input("Press enter to continue")
			print("\n------------------------------------")
			print("\nThe computer attacked")
			computerSearch(gameplay, obj_player)
			print("\nEnemy field:")
			print_board(obj_comp)
			print("\nYour field:")
			print_board(obj_player)
			checkGameIsWon(gameplay, obj_player)
			printSurvivingShips(obj_player, obj_comp)

			gameplay.turn = 1


#-----------------------------attacking-----------------------------

"""takes desired attack location and checks if it is a hit
if hit, proceed with \\hit(...)
Only points that haven't yet been attacked get here"""
def selectedAttack(attackPoint, gameplay, obj):
	obj.alreadyAttacked.append(deepcopy(attackPoint))
	for x in range(len(obj.ships)):
		for y in range(len(obj.ships[x].location)):
			if attackPoint == obj.ships[x].location[y]:  # hit
				obj.previousHits.append(attackPoint)
				hit(attackPoint, obj.board, obj.ships[x])
				# differentShipAttacked(attackPoint, gameplay, obj)
				checkIfShipSank(gameplay, obj.ships, obj.ships[x], obj.sunk)
				return obj
	print("The attack was at", str(attackPoint)+'.', "It missed\n")  # I want a better message
	obj.board[attackPoint[0]][attackPoint[1]] = 'M'


"""confirmed hit, changes hit values in object, changes board"""
def hit(attackPoint, obj_board, ship):
	for i in range(2):
		if attackPoint[i] - ship.start[i] == 0:
			ship.hits[(attackPoint[((i+1)%2)] - ship.start[((i+1)%2)])] = 1
	
	print("\nHit at" , attackPoint)
	ship.life = int(ship.life - (100 / len(ship.hits)))
	obj_board[attackPoint[0]][attackPoint[1]] = 'X'


def checkIfShipSank(gameplay, objShips, ship, objSunk):
	if ship.life <= 15:	 # no ships will be considered alive if above 15pts (standard set incase a ship's life != exactly 0)
		if gameplay.turn == 1:
			print("You sank the enemy" , ship.name , "\n")
		else:
			print("The enemy sank your" , ship.name , "\n")
			gameplay.targetingOff()
			gameplay.circlingOff()
		for point in ship.location:
			if point in gameplay.computerShouldPursue:
				gameplay.computerShouldPursue.remove(point)
		objSunk.append(ship)
		objShips.remove(ship)
		return gameplay


#-------------------------------player------------------------------

def playForMe(gameplay, obj):  # testing
	while True:  # testing
		turn = len(obj.alreadyAttacked)+1  # testing
		attackPoint = [int(((turn-(turn%9))/9)+1), int((turn%9)+1) ]  # testing
		print(attackPoint)  # testing
		if not validPoint(attackPoint, obj):  # testing
			sys.exit(0)  # testing
		else:  # testing
			selectedAttack(attackPoint, gameplay, obj)  # testing
			break  # testing


def playersTurn(gameplay, obj):
	print("\nIt's your turn.")
	while True:  # loop to keep player's input correct
		# backdoor to skip having to play for self
		if not obj.alreadyAttacked:
			backdoor = input("Please enter an attack coordinate  eg 4 , 3\nWhere would you like to attack?\t\t")
			try:
				attackPoint = [int(x) for x in backdoor.split(",")]
			except:
				if backdoor == "computer_play_for_me".rstrip():
					gameplay.computerPlayForMe = True
					break
				else:
					print("\nThat is an incorrect input. Please try again")
					continue
		else:	
			try:
				attackPoint = [int(x) for x in input("Please enter an attack coordinate  eg 4 , 3\nWhere would you like to attack?\t\t").split(",")]  # set input as list 
			except:
			 	print("\nThat is an incorrect input. Please try again")
			 	continue
		print("\n------------------------------------")		#aestetic
		if len(attackPoint) != 2:
			print("\nYou entered too many coordinates")
		if not validPoint(attackPoint, obj):  # prevents an input not on board
			if any(attackPoint == i for i in obj.alreadyAttacked):  # prevents attacking same square
				print("\nYou have already attacked there.  Please try again")
			else:
				print("\nYour attack was not on the board.  Please try a location that makes more sense") 
		else:
			selectedAttack(attackPoint, gameplay, obj)
			break


#------------------------------computer-----------------------------

"""gameplay of computer trying to attack go across as an x, then after 17 (9 then 8) shots,
 begin blank area search determine the blank areas that are suitable for ship sizes (use a 
 list of fired on location and remaining ship lengths) blank areas"""
def computerSearch(gameplay, obj):
	if gameplay.targeting: attackPoint = targeting(gameplay, obj)
	elif gameplay.circling:	attackPoint = circle(gameplay, obj)
	elif gameplay.computerShouldPursue:
		gameplay.circlingOn(gameplay.computerShouldPursue[0])
		gameplay.computerShouldPursue.remove(gameplay.computerShouldPursue[0])
		attackPoint = circle(gameplay, obj)
	elif len(gameplay.crossPattern) > 0:  # should pursue is empty, but crossPatter not, so pursue those
		attackPoint = gameplay.crossPattern[randint(0,len(gameplay.crossPattern)-1)]
		gameplay.crossPattern.remove(attackPoint)
		if attackIsNewHit(attackPoint, obj): gameplay.circlingOn(attackPoint)
	else:  # crossPattern, ships to pursue: empty
		attackPoint = find_hidden_ships(obj)
		if attackIsNewHit(attackPoint, obj): gameplay.circlingOn(attackPoint)
	if attackPoint in gameplay.crossPattern: gameplay.crossPattern.remove(attackPoint)
	selectedAttack(attackPoint, gameplay, obj)


"""shoots around a known hit (left, up, right, down) until more of ship found.  If different ship hit, save it for later.
 Process will only go up to 3 because if 3 has already been hit, targeting or should have already taken care of start. """
def circle(gameplay, obj):
	hasAlreadyBeenAttacked = True 
	surroundings = [[0, -1], [-1, 0], [0, 1], [1, 0]]
	while hasAlreadyBeenAttacked:
		attackPoint = [gameplay.initialHit[0] + surroundings[gameplay.process][0], gameplay.initialHit[1] + surroundings[gameplay.process][1]]  #where the computer tries to attack 
	
		if attackPoint in gameplay.crossPattern: gameplay.crossPattern.remove(attackPoint)
		
		# the attack point has not been attacked already and is good to be returned
		if validPoint(attackPoint, obj):
			hasAlreadyBeenAttacked = False 
			# we have found a ship for targeting
			if isSameShip(attackPoint, gameplay, obj):
				gameplay.orientation = deepcopy(((gameplay.process+1)%2))
				gameplay.targetingOn(attackPoint)
				return attackPoint
			if attackIsNewHit(attackPoint, obj): gameplay.computerShouldPursue.append(deepcopy(attackPoint))  # but not the ship we want
		gameplay.process += 1 
	return attackPoint


"""once an orientation has been found, attack along that orientation"""
def targeting(gameplay, obj):
	if len(gameplay.nextTo) == 0:  # the function does not have ability to find rest of ships
		attackPoint = shipKiller(gameplay, obj)
		return attackPoint

	if gameplay.firstHit[gameplay.orientation] < gameplay.previousHit[gameplay.orientation] and -1 in gameplay.nextTo:
		gameplay.nextTo.remove(-1)  # no point in attacking to the left/up if start was already the left/up most point

	attackPoint = deepcopy(gameplay.previousHit)
	attackPoint[gameplay.orientation] = attackPoint[gameplay.orientation] + gameplay.nextTo[0]  # deepcopy?
	
	if isSameShip(attackPoint, gameplay, obj) == False or \
attackPoint[((gameplay.orientation+1)%2)] == 9 or attackPoint[((gameplay.orientation+1)%2)] == 1:
		del gameplay.nextTo[0]
	
	if attackPoint not in obj.alreadyAttacked and attackPoint[gameplay.orientation] > 0 and attackPoint[gameplay.orientation] < obj.boardSize:
		if attackIsNewHit(attackPoint, obj) and not isSameShip(attackPoint, gameplay, obj):
			gameplay.computerShouldPursue.append(deepcopy(attackPoint))
		return attackPoint
	elif attackPoint in obj.alreadyAttacked and pointOverIsGood(attackPoint, gameplay, obj):
		tempPoint = attackPoint
		tempPoint[gameplay.orientation] = (tempPoint[gameplay.orientation] + gameplay.nextTo[0])
		gameplay.previousHit = tempPoint
		return tempPoint
	elif attackPoint[gameplay.orientation] == 1 and len(gameplay.nextTo) == 2:
		del gameplay.nextTo[0]
		attackPoint = gameplay.firstHit
		attackPoint[gameplay.orientation] = attackPoint[gameplay.orientation] + gameplay.nextTo[0]
	else:
		del gameplay.nextTo[0]
		attackPoint = shipKiller(gameplay, obj)
	
	gameplay.previousHit = attackPoint
	return attackPoint

""""check if the following point (the point next to a hit) is worth  is worth attacking
used incase a point was blocked off during the targeting/circling of another ship"""
def pointOverIsGood(attackPoint, gameplay, obj):
	if (attackPoint[gameplay.orientation] > 1 or attackPoint[gameplay.orientation] < 9):
		attackPoint = attackPoint[gameplay.orientation] + gameplay.nextTo[0]
		if isSameShip(attackPoint, gameplay, obj): return True
	return False

"""used to clean up any parts of a ship that are unfindable by the targeting algorithm"""
def shipKiller(gameplay, obj):
	for ship in obj.ships:
			if gameplay.firstHit in ship.location:
				for point in ship.location:
					if obj.board[point[0]][point[1]] != 'X': return point




#-------------------------------utility-----------------------------

"""point has not been attacked and is in a ship's location"""
def attackIsNewHit(attackPoint, obj):
	for ship in obj.ships:
		if any(attackPoint == point for point in ship.location):
			if attackPoint not in obj.alreadyAttacked: return True
	return False

"""end game if game is won"""
def checkGameIsWon(gameplay, obj):
	if not obj.ships:
		if gameplay.turn:
			print("You won!")
			sys.exit(0)
		print("You lost")
		sys.exit(0)

"""both hits are in the same field, and not starting point"""
def isSameShip(attackPoint, gameplay, obj):
	for ship in obj.ships:
		if gameplay.targeting:
			if attackPoint in ship.location and gameplay.firstHit in ship.location and attackPoint != gameplay.initialHit:
				return True 
		if gameplay.circling:
			if attackPoint in ship.location and gameplay.initialHit in ship.location and attackPoint != gameplay.initialHit:
				return True 
	return False

def print_board(obj):
	for row in obj.board:
		print("  ".join(str(char) for char in row))


def printSurvivingShips(obj_player, obj_comp):	#display ships and their hits of computer and player
	print("Your fleet status is:")
	for i in obj_player.ships:
		print(i.name , "\t:", "Hits:\t", i.hits, "\tRemaining life: ", i.life)
	print("\nYou have sunk: ")
	for i in obj_comp.sunk:
		print(i.name , end = "\t\t")
	print("\n")
	# print("\n\nRemaining enemy ships are:")
	# for i in ships.computer:
	# 	print(i.name , end = "\t\t")

"""display repeated coordinates"""
def testFunction(anotherList):  # testing
	seenFirst = set()  # testing
	alreadySeen = set()  # testing
	first_tuple_list = [tuple(lst) for lst in anotherList]  # testing
	for x in first_tuple_list:  # testing
		if x not in seenFirst:  # testing
			seenFirst.add(x)  # testing
		else:  # testing
			alreadySeen.add(x)  # testing
	print(alreadySeen)  # testing

"""print ship locations"""
def testing(obj_comp, obj_player):  # testing
	testList1 = []  # testing
	for i in obj_comp.ships:  # testing
		print(i.location)  # testing
		testList1.extend(i.location)  # testing

	testList2 = []  # testing
	for i in obj_player.ships:  # testing
		print(i.location)  # testing
		testList2.extend(i.location)  # testing
	return testList1, testList2  # testing


#has not been attacked, within board
def validPoint(attackPoint, obj):
	if attackPoint not in obj.alreadyAttacked and all(0 < i < obj.boardSize for i in attackPoint): return True 
	return False

#-------------------------------------------------------------------
def main():
	computer = Computer()
	player = Player()
	
	create_board(computer)	
	
	createEnemysShips(computer)  # iterate through ships.definition to create computer ships
	shipGenerationOption(player)
	# generatePlayersShips(player)  # testing
	# createPlayersShips(player)  # ignore \\shipGenerationOption(.)

	# testList1, testList2 = testing(computer, player)  # testing
	# testFunction(testList2)		# testing
	

	isTurn(computer, player)

#--------------TESTING------------------

main()
#HiShayaniiii