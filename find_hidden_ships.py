# read in board
# calculate areas for hiding (nevere attacked) \\distance_calculator(.)
# store info as list:  [list], list = [[area able to be attacked]], area able to be attacked = [[[coordinates of area], length of area]]
# pass info and compare with largest ship size.  If ship can fit in that area, try attacking its midpoint


def find_hidden_ships(obj):
	lengths_of_empty_board = distance_calculator(obj)
	max_size = max_ship_size(obj)
	for i in lengths_of_empty_board:
		if i[1] >= max_size:
			middle_point = round(max_size/2)
			return i[0][middle_point]


def max_ship_size(obj):
	shipSize = 0
	for ship in obj.ships:
		if ship.size > shipSize: shipSize = ship.size
	return shipSize

def distance_calculator(obj):	
	points = []
	count = 0
	horizontal_board = []

	for i in range(obj.boardSize):
		for j in range(obj.boardSize):
			if i == 0 or j == 0: continue

			if obj.board[i][j] == "~" or obj.board[i][j] == "S":
				count += 1 
				points.append([i,j])
				if j == 9 and count > 1:
					horizontal_board.append([points, count])
				elif j ==9:
					pass
				else:
					continue
			elif count == 1 and obj.board[i][j] == "X" and obj.board[i][j] == "M": pass
			elif (obj.board[i][j] != "~" or obj.board[i][j] == "S") or j == 9: 
				horizontal_board.append([points, count])
			points = []
			count = 0

	for j in range(obj.boardSize):
		for i in range(obj.boardSize):
			if i == 0 or j == 0: continue

			if obj.board[i][j] == "~" or obj.board[i][j] == "S":
				count += 1 
				points.append([i,j])
				if i == 9 and count > 1:
					horizontal_board.append([points, count])
				elif i ==9:
					pass
				else:
					continue
			elif count == 1 and obj.board[i][j] == "X" and obj.board[i][j] == "M": pass
			elif (obj.board[i][j] != "~" or obj.board[i][j] == "S") or i == 9: 
				horizontal_board.append([points, count])
			points = []
			count = 0

	return horizontal_board