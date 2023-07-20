from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


class aSearch:
    # Creation of Grid with no parameters
    def __init__(self, x: int, y: int):
        board = []
        for i in range(x):
            tempRow = []
            for j in range(y):
                tempRow.append(1)
            board.append(tempRow)
        self.tempBoard = board

    # Add obstacles into the board and convert it to a grid
    def obstacles(self, danger):
        for pos in danger:
            # print(pos)
            self.tempBoard[int(10 - pos['y'])][int(pos['x'])] = 0
        self.board = Grid(matrix=self.tempBoard) # Grid for the A* algorithm to find the nearest pellet
        # print(self.board.grid_str())

    # starFinder will use A* to find the closest path to the provided pellet and instruct the snake what path to take
    def starFinder(self, headX, headY, pelletX, pelletY):
        start = self.board.node(headX, headY) # Where snake head is
        end = self.board.node(pelletX, pelletY) # Where end of the snake is

        finder = AStarFinder()
        path, runs = finder.find_path(start, end, self.board)
        # print(path)

        if len(path) >= 2:
            current = path[0]
            next = path[1]


            print(self.board.grid_str(path=path, start=start, end=end))
            # Go right
            if current[0] < next[0]:
                return 'right'
            # Left
            elif current[0] > next[0]:
                return 'left'

            # NOTE: THINK WITH Y GOING BOTTOM TO TOP!
            # Down
            elif current[1] < next[1]:
                return 'down'
            # Up
            else:
                return 'up'

        else:
            return 'NO DIRECTION'

    # cleanup will clear the grid of obstacles for the next move
    def cleanup(self, danger):
        for pos in danger:
            # print(pos)
            self.tempBoard[int(10 - pos['y'])][int(pos['x'])] = 1
        self.board = Grid(matrix=self.tempBoard)
        # print("Did the board clean itself?")
        # print(self.board.grid_str())
