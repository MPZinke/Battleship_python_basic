from random import randint, seed
# seed(90)  #testing  12545, 8012

boardSize = 10

class enemyShip:
	def __init__(self, name , size, tempShips):
		self.life = 100
		self.name = name
		self.size = size
		self.orientation = randint(0,1)			#0 is horizontally placing, 1 is vertically placing
		self.direction , self.hits , self.location , self.start = computerStart(self.orientation, self.size, tempShips) 

class playerShip:
	def __init__(self, name, orientation, size, start, tempShips):
		direction = 0
		hits = []
		location = []
		self.life = 100
		self.name = name
		self.orientation = orientation
		self.size = size
		self.start = start
		self.direction , self.hits , self.location , self.start = placeShip(direction, hits, location, self.orientation, self.size, self.start, tempShips) 
#direction, hits, location, 

def computerStart(orientation, size, tempShips):
	# seed(123)  #testing
	direction = 0  # superficial value
	hits = []  #list of hits returned to object
	location = []  # list of ships location returned to object edited and passed to isSameLoation, then returned and assigned to location
	start = list()
	start.append(randint(1,9))
	start.insert(((orientation+1)%2), randint(1, (boardSize-1)-size))
	direction, hits, location, start = placeShip(direction, hits, location, orientation, size, start, tempShips)
	return direction, hits, location, start

def placeShip(direction, hits, location, orientation, size, start, tempShips):
	if start[orientation] <= 5:								#if row less than 5
		direction = 1								#increase row/column (right/down) if start is left/top
	else:
		direction = -1								#decrease row/column (left/up) if start is right/botto
	for i in range(0, size):			#iterate through size of ship, makes the "parts, (iterations), and assembles
		hits.append(0)					#add to hit array (when all are true, ship = sunk) through ship size iteration
		location.append([start[0] + (i * (orientation%2)), start[1] + (i * ((orientation+1)%2))]) 
	direction, location, orientation, start = checkIfShipsOverlap(direction, location , orientation, size, start, tempShips)			#determines if ships overlap and moves them
	return direction , hits , location , start 

# move against orientation if overlap with another ship
def checkIfShipsOverlap(direction, location, orientation, size, start, tempShips):			
	shipLocations = []			#***	list of all ship locations for showing overlap
	for ship in tempShips:		#adds all constructed ships' locations to list to determine if needs to be moved 
		shipLocations.extend(ship.location)
	# finds if any coordinate already assigned, too high, too low
	while any(i in shipLocations for i in location) or any(j == 0 for i in location for j in i) or any(j == boardSize for i in location for j in i):		#finds if any coordinates already assigned	
		for y in range(0, len(location)):					#move ship process
			location[y][orientation] = location[y][orientation] + direction		#shift up/down
		direction , location , orientation = checkIfOutOfRange(direction , location , orientation , size)	#if initial move does not work, this performs unlikely cases
		start = location[0]
	del shipLocations[:]
	return direction , location , orientation , start

# probably unnecessary function
def checkIfOutOfRange(direction, location, orientation, size):		#used when ship becomes out of range and shifts its direction
	def whatOrientation(orientation):		#change from left/right to up/down
		orientation = (orientation+1)%2
		return orientation
	for binary in range(2):
		if any(location[i][binary] == boardSize for i in range(len(location))):	#out of bounds too low
			for y in range(size):					
				location[y][binary] = location[y][binary] - 1
			direction = -1
			oreintation = whatOrientation(orientation)
		elif any(location[i][binary] == 0 for i in range(len(location))):	#out of bounds too high
			for y in range(size):
				location[y][binary] = location[y][binary] + 1	
			direction = 1
			orientation = whatOrientation(orientation)
	return direction , location , orientation
