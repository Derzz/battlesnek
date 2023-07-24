from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import typing
import random

class priorASearch:
    def food(game_state: typing.Dict) -> typing.Dict:
        is_move_safe = {"up": True, "down": True, "left": True, "right": True}
        print(f"Turn {game_state['turn']}")

        # Note: A* will only be searching for 9 x 9 area, it will treat the edges as
        xBoard, yBoard = game_state["board"]["height"], game_state["board"]["width"]
        searchObj = aSearch(xBoard, yBoard)
        my_head = game_state["you"]["body"][0]  # Coordinates of your head
        my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

        x = my_head["x"]
        y = my_head["y"]

        # danger is a list containing all positions that are dangerous to our current snake which incluedes the bodies of other snakes and our body
        danger = []
        danger.clear()

        # These two loops will determine what is dangerous to the snake and will be provided to A* to not go near them
        for snake in game_state['board']['snakes'][1:]:
            for body in snake['body']:
                print(f"Rival snake body and head {body}")
                danger.append(body)
            if snake['length'] < game_state['you']['length']:
                danger.remove(snake['head'])
        myBody = game_state['you']['body']
        # print(myBody)
        for body in myBody[1:]:
            # print(f"My snake body {body}")
            danger.append(body)

        searchObj.obstacles(danger)
        shortestDist, shortestX, shortestY = 9999, 0, 0
        y = 10 - y

        # This will provide the closest pellet to the snake based on their manhattan distances
        # If no pellet can be found, border_wrap() will be called and the snake will determine a safe move to go in
        pelletList = game_state['board']['food']
        while pelletList:

            for pellet in pelletList:
                # If turn is greater than 3, snake will not consider border pellets anymore, as it's too risky since the full snake is out
                xPellet, yPellet = pellet['x'], 10 - pellet['y']
                if (xPellet == 0 or yPellet == 0 or xPellet == xBoard - 1 or yPellet == yBoard - 1) and game_state[
                    'turn'] > 3:
                    print(f"removing {pellet}")
                    pelletList.remove(pellet)
                else:
                    manDist = abs(x - xPellet) + abs(y - yPellet)
                    if manDist < shortestDist: shortestDist, shortestX, shortestY = manDist, xPellet, yPellet

            tempNext_move = searchObj.starFinder(x, y, shortestX, shortestY)

            if tempNext_move == 'NO DIRECTION':
                pelletList.remove(pellet)
            else:
                searchObj.cleanup(danger)
                print(f"MOVE {game_state['turn']}: {tempNext_move}")
                return {"move": tempNext_move}

        return priorASearch.border_wrap(game_state, is_move_safe)

    # border_wrap will attempt to wrap around the border for the snake until a safe pellet can be found in future moves
    def border_wrap(game_state: typing.Dict, is_move_safe: dict):
        # First take possible moves from next_move and determine valid directions
        print("No available pellet can be found! Wrapping around!")

        my_head = game_state["you"]["body"][0]  # Coordinates of your head
        my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"
        my_tail = game_state["you"]["body"][-1]  # Coordinates of your tail

        board_width = game_state['board']['width']
        board_height = game_state['board']['height']

        fed = game_state['you']['health'] == 100

        x = my_head["x"]
        y = my_head["y"]
        px = my_neck["x"]
        py = my_neck["y"]

        rx = my_head["x"] + 1
        ry = my_head["y"]
        lx = my_head["x"] - 1
        ly = my_head["y"]
        ux = my_head["x"]
        uy = my_head["y"] + 1
        dx = my_head["x"]
        dy = my_head["y"] - 1
        move_list_1 = priorASearch.calc_move(game_state, x, y, px, py, board_width, board_height, fed)
        if (priorASearch.is_single_move(move_list_1)):
            next_move = move_list_1
        elif (len(move_list_1) > 0):
            next_move = random.choice(move_list_1)
        else:
            next_move = priorASearch.end_it(game_state)
        return {"move": next_move}

    def check_move(game_state: typing.Dict, x, y, px, py, board_width, board_height, fed):
        my_head = game_state["you"]["body"][0]  # Coordinates of your head
        my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

        is_move_safe = {"up": True, "down": True, "left": True, "right": True}

        if px < x:  # Neck is left of head, don't move left
            is_move_safe["left"] = False
        elif px > x:  # Neck is right of head, don't move right
            is_move_safe["right"] = False
        elif py < y:  # Neck is below head, don't move down
            is_move_safe["down"] = False
        elif py > y:  # Neck is above head, don't move up
            is_move_safe["up"] = False

        battlesnakes = game_state['board']['snakes']
        for snake in battlesnakes:
            for bodyCoord in snake['body'][:(fed - 1)]:
                if is_move_safe['right'] and (
                        [x + 1, y] == [bodyCoord['x'], bodyCoord['y']] or x + 1 >= board_width - 1):
                    is_move_safe['right'] = False
                if is_move_safe['left'] and ([x - 1, y] == [bodyCoord['x'], bodyCoord['y']] or x - 1 <= 0):
                    is_move_safe['left'] = False
                if is_move_safe['up'] and ([x, y + 1] == [bodyCoord['x'], bodyCoord['y']] or y + 1 >= board_height - 1):
                    is_move_safe['up'] = False
                if is_move_safe['down'] and ([x, y - 1] == [bodyCoord['x'], bodyCoord['y']] or y - 1 <= 0):
                    is_move_safe['down'] = False

        safe_moves = []
        for move, isSafe in is_move_safe.items():
            if isSafe:
                safe_moves.append(move)
        return safe_moves

    def check_move_failsafe(game_state: typing.Dict, x, y, px, py, board_width, board_height, fed):
        print("Failsafe on")

        my_head = game_state["you"]["body"][0]  # Coordinates of your head
        my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

        is_move_safe = {"up": True, "down": True, "left": True, "right": True}

        if px < x:  # Neck is left of head, don't move left
            is_move_safe["left"] = False
        elif px > x:  # Neck is right of head, don't move right
            is_move_safe["right"] = False
        elif py < y:  # Neck is below head, don't move down
            is_move_safe["down"] = False
        elif py > y:  # Neck is above head, don't move up
            is_move_safe["up"] = False

        battlesnakes = game_state['board']['snakes']
        for snake in battlesnakes:
            for bodyCoord in snake['body'][:(fed - 1)]:
                if [x + 1, y] == [bodyCoord['x'], bodyCoord['y']] or x + 1 > board_width - 1:
                    is_move_safe['right'] = False
                if [x - 1, y] == [bodyCoord['x'], bodyCoord['y']] or x - 1 < 0:
                    is_move_safe['left'] = False
                if [x, y + 1] == [bodyCoord['x'], bodyCoord['y']] or y + 1 > board_height - 1:
                    is_move_safe['up'] = False
                if [x, y - 1] == [bodyCoord['x'], bodyCoord['y']] or y - 1 < 0:
                    is_move_safe['down'] = False
        safe_moves = []
        for move, isSafe in is_move_safe.items():
            if isSafe:
                safe_moves.append(move)
        return safe_moves

    def calc_move(game_state: typing.Dict, x, y, px, py, board_width, board_height, fed):
        safe_moves = priorASearch.check_move(game_state, x, y, px, py, board_width, board_height, fed)

        if len(safe_moves) > 0:
            return safe_moves
        else:
            safe_moves = priorASearch.check_move_failsafe(game_state, x, y, px, py, board_width, board_height, fed)
            if (len(safe_moves) > 0):
                return safe_moves
            else:
                return priorASearch.end_it(game_state)

    def is_single_move(var):
        if var == "right" or var == "left" or var == "up" or var == "down":
            return True
        else:
            return False

    def end_it(game_state: typing.Dict):
        my_head = game_state["you"]["body"][0]  # Coordinates of your head
        my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"
        # End it
        print(f"MOVE {game_state['turn']}: I will go out on my own terms!")
        if my_neck["x"] < my_head["x"]:  # Neck is left of head, move left
            return "left"
        elif my_neck["x"] > my_head["x"]:  # Neck is right of head, move right
            return "right"
        elif my_neck["y"] < my_head["y"]:  # Neck is below head, move down
            return "down"
        elif my_neck["y"] > my_head["y"]:  # Neck is above head, move up
            return "up"
        else:
            return "down"


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
