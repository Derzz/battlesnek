# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing

# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "pixelsnek",  # TODO: Your Battlesnake Username
        "color": "#947706",  # TODO: Choose color
        "head": "fang",  # TODO: Choose head
        "tail": "horse",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"
    my_tail = game_state["you"]["body"][-1]  # Coordinates of your tail

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    # Combined with
    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    # Combined with
    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes

    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

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

    move_list_1 = calc_move (game_state, x, y, px, py, board_width, board_height)
    if (is_single_move (move_list_1)):
        next_move = move_list_1
    elif (len (move_list_1) > 0):
        next_move = random.choice (move_list_1)
    else:
        next_move = end_it (game_state)

    #Food hunting
    food = game_state['board']['food']
    for pellet in food:
        if is_move_safe['right'] and [rx, ry] == [pellet['x'], pellet['y']]:
            next_move = "right"
            break
        elif is_move_safe['left'] and [lx, ly] == [pellet['x'], pellet['y']]:
            next_move = "left"
            break
        elif is_move_safe['up'] and [ux, uy] == [pellet['x'], pellet['y']]:
            next_move = "up"
            break
        elif is_move_safe['down'] and [dx, dy] == [pellet['x'], pellet['y']]:
            next_move = "down"
            break
        else:
            if game_state["you"]["health"] == 1:
                return {"move": end_it}
    
    # Tail chasing
    if game_state["you"]["health"] > 25 and game_state["you"]["health"] != 100 and game_state["you"]["length"] % 2 == 0:
        if is_move_safe['right'] and [rx, ry] == [my_tail['x'], my_tail['y']]:
            next_move = "right"
        if is_move_safe['left'] and [lx, ly] == [my_tail['x'], my_tail['y']]:
            next_move = "left"
        if is_move_safe['up'] and [ux, uy] == [my_tail['x'], my_tail['y']]:
            next_move = "up"
        if is_move_safe['down'] and [dx, dy] == [my_tail['x'], my_tail['y']]:
            next_move = "down"

    if game_state["you"]["health"] == 1:
        next_move = end_it
    
    # TODO: Step 3A - Don't ram into heads where opponent.snake.len > ours

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = game_state['board']['food']

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}

def check_move (game_state: typing.Dict, x, y, px, py, board_width, board_height):
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
        for bodyCoord in snake['body'][:-1]:
            if is_move_safe['right'] and ([x+1, y] == [bodyCoord['x'], bodyCoord['y']] or x+1 >= board_width - 1):
                is_move_safe['right'] = False
            if is_move_safe['left'] and ([x-1, y] == [bodyCoord['x'], bodyCoord['y']] or x-1 <= 0):
                is_move_safe['left'] = False
            if is_move_safe['up'] and ([x, y+1] == [bodyCoord['x'], bodyCoord['y']] or y+1 >= board_height - 1):
                is_move_safe['up'] = False
            if is_move_safe['down'] and ([x, y-1] == [bodyCoord['x'], bodyCoord['y']] or y-1 <= 0):
                is_move_safe['down'] = False
                
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)
    return safe_moves

def check_move_failsafe (game_state: typing.Dict, x, y, px, py, board_width, board_height):
    print ("Failsafe on")
    
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
        for bodyCoord in snake['body'][:-1]:
            if [x+1, y] == [bodyCoord['x'], bodyCoord['y']] or x+1 > board_width - 1:
                is_move_safe['right'] = False
            if [x-1, y] == [bodyCoord['x'], bodyCoord['y']] or x-1 < 0:
                is_move_safe['left'] = False
            if [x, y+1] == [bodyCoord['x'], bodyCoord['y']] or y+1 > board_height - 1:
                is_move_safe['up'] = False
            if [x, y-1] == [bodyCoord['x'], bodyCoord['y']] or y-1 < 0:
                is_move_safe['down'] = False
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)
    return safe_moves

def calc_move (game_state: typing.Dict, x, y, px, py, board_width, board_height):
    safe_moves = check_move (game_state, x, y, px, py, board_width, board_height)

    if len (safe_moves) > 0:
        return safe_moves
    else:
        safe_moves = check_move_failsafe (game_state, x, y, px, py, board_width, board_height)
        if (len (safe_moves) > 0):
            return safe_moves
        else:
            return end_it (game_state)

def foresight (game_state: typing.Dict, x, y, px, py, board_width, board_height):
    battlesnakes = game_state['board']['snakes']
    for snake in battlesnakes:
        for bodyCoord in snake['body'][:-1]:
            return len (calc_move (game_state, x, y, px, py, board_width, board_height)) > 0

def is_single_move (var):
    if var == "right" or  var == "left" or  var == "up" or  var == "down":
        return True
    else:
        return False

def end_it (game_state: typing.Dict):
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

    run_server({"info": info, "start": start, "move": move, "end": end}, 8001)