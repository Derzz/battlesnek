# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#

# This snake will focus on using the A* algorithm to find the nearest pellet to it.

import random
import typing
import search
from search import aSearch

# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "pixelsnek",
        "color": "#947706",
        "head": "fang",
        "tail": "horse",
    }



# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    xBoard, yBoard = game_state["board"]["height"], game_state["board"]["width"]
    global searchObj
    searchObj = aSearch(xBoard, yBoard)



    print("SUCCESSFULLY IMPLEMENTED GRAPH AND NODES")
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}
    print(f"Turn {game_state['turn']}")

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"
    my_tail = game_state["you"]["body"][-1]  # Coordinates of your tail

    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    fed = 0

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

    # move_list_1 = calc_move(game_state, x, y, px, py, board_width, board_height, fed)
    # if (is_single_move(move_list_1)):
    #     next_move = move_list_1
    # elif (len(move_list_1) > 0):
    #     next_move = random.choice(move_list_1)
    # else:
    #     next_move = end_it(game_state)

    #TODO Implement A* algorithm
    #TODO Implement aggressiveness as needed(Aka our strategy)

    # danger is a list containing all positions that are dangerous to our current snake which incluedes the bodies of other snakes and our body
    danger = []
    danger.clear()

    #TODO Implement what to do with other snake heads

    # These two loops will determine what is dangerous to the snake and will be provided to A* to not go near them
    for snake in game_state['board']['snakes'][1:]:
        for body in snake['body']:
            print(f"Rival snake body and head {body}")
            danger.append(body)

    myBody = game_state['you']['body']
    #print(myBody)
    for body in myBody[1:]:
        print(f"My snake body {body}")
        danger.append(body)


    global searchObj
    searchObj.obstacles(danger)
    shortestDist, shortestX, shortestY = 9999, 0, 0
    y = 10 - y

    # This will provide the closest pellet to the snake based on their manhattan distances
    # If no pellet can be found, border_wrap() will be called
    pelletList = game_state['board']['food']
    while pelletList:

        # TODO If pellet would result in the snake trapping itself, do not attempt to go for it

        for pellet in pelletList:
            xPellet, yPellet = pellet['x'], 10 - pellet['y']
            manDist = abs(x - xPellet) + abs(y - yPellet)
            if manDist < shortestDist: shortestDist, shortestX, shortestY = manDist, xPellet, yPellet


        tempNext_move = searchObj.starFinder(x, y, shortestX, shortestY)

        if tempNext_move == 'NO DIRECTION':
            pelletList.remove(pellet)
        else:
            searchObj.cleanup(danger)
            print(f"MOVE {game_state['turn']}: {tempNext_move}")
            return {"move": tempNext_move}


    return border_wrap(game_state, is_move_safe)

# TODO Under Works
# border_wrap will attempt to wrap around the border for the snake until a safe pellet can be found in future moves
def border_wrap(game_state: typing.Dict, is_move_safe: dict):
    # TODO Make Snake wrap around border until pellet can be found
    # First take possible moves from next_move and determine valid directions
    print("No available pellet can be found! Wrapping around!")
    return {"move:" 'down'}

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
            if is_move_safe['right'] and ([x + 1, y] == [bodyCoord['x'], bodyCoord['y']] or x + 1 >= board_width - 1):
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
    safe_moves = check_move(game_state, x, y, px, py, board_width, board_height, fed)

    if len(safe_moves) > 0:
        return safe_moves
    else:
        safe_moves = check_move_failsafe(game_state, x, y, px, py, board_width, board_height, fed)
        if (len(safe_moves) > 0):
            return safe_moves
        else:
            return end_it(game_state)


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


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
