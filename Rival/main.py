# This is the Rival Snake that is meant to defeat us. The strategy for this snake is to go around in circles until it's health is < 25%. After that, it will go for food.
# AKA: This is a very defensive snake that our aggressive snake needs to fight.

import random
import typing


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

    move_list_1 = calc_move(game_state, x, y, px, py, board_width, board_height, fed)
    if (is_single_move(move_list_1)):
        next_move = move_list_1
    elif (len(move_list_1) > 0):
        next_move = random.choice(move_list_1)
    else:
        next_move = end_it(game_state)

    # Food hunting
    food = game_state['board']['food']
    for pellet in food:
        if is_move_safe['right'] and [rx, ry] == [pellet['x'], pellet['y']]:
            next_move = "right"
            fed = 1
            break
        elif is_move_safe['left'] and [lx, ly] == [pellet['x'], pellet['y']]:
            next_move = "left"
            fed = 1
            break
        elif is_move_safe['up'] and [ux, uy] == [pellet['x'], pellet['y']]:
            next_move = "up"
            fed = 1
            break
        elif is_move_safe['down'] and [dx, dy] == [pellet['x'], pellet['y']]:
            next_move = "down"
            fed = 1
            break
        else:
            fed = 0

    # Tail chasing
    if game_state["you"]["health"] > 25 and game_state["you"]["length"] >= 5:
        if is_move_safe['right'] and [rx, ry] == [my_tail['x'], my_tail['y']]:
            next_move = "right"
        if is_move_safe['left'] and [lx, ly] == [my_tail['x'], my_tail['y']]:
            next_move = "left"
        if is_move_safe['up'] and [ux, uy] == [my_tail['x'], my_tail['y']]:
            next_move = "up"
        if is_move_safe['down'] and [dx, dy] == [my_tail['x'], my_tail['y']]:
            next_move = "down"

    # move_list_2 = []
    # if is_single_move (move_list_1):
    #     print ("Case 1")
    #     next_move = move_list_1
    #     if move_list_1 == "right" and not foresight(game_state, rx, ry, x, y, board_width, board_height):
    #         # He's screwed.
    #             print(f"MOVE {game_state['turn']}: Oh no. ")
    #     elif move_list_1 == "left" and not foresight(game_state, lx, ly, x, y, board_width, board_height):
    #         # He's screwed.
    #             print(f"MOVE {game_state['turn']}: Oh no. ")
    #     elif move_list_1 == "up" and not foresight(game_state, ux, uy, x, y, board_width, board_height):
    #         # He's screwed.
    #             print(f"MOVE {game_state['turn']}: Oh no. ")
    #     elif move_list_1 == "down" and not foresight(game_state, dx, dy, x, y, board_width, board_height):
    #         # He's screwed.
    #             print(f"MOVE {game_state['turn']}: Oh no. ")
    # elif len (move_list_1) > 0:
    #     print ("Case 2")
    #     for move in move_list_1:
    #         if move == "right" and not foresight(game_state, rx, ry, x, y, board_width, board_height):
    #             print ("2.1")
    #             is_move_safe ["right"] = False
    #         elif move == "left" and not foresight(game_state, lx, ly, x, y, board_width, board_height):
    #             print ("2.2")
    #             is_move_safe ["left"] = False
    #         elif move == "up" and not foresight(game_state, ux, uy, x, y, board_width, board_height):
    #             print ("2.3")
    #             is_move_safe ["up"] = False
    #         elif move == "down" and not foresight(game_state, dx, dy, x, y, board_width, board_height):
    #             print ("2.4")
    #             is_move_safe ["down"] = False
    #     for move, isSafe in is_move_safe.items():
    #         if isSafe:
    #             move_list_2.append(move)
    #     if is_single_move (move_list_2):
    #         next_move = move_list_2
    #     elif (len(move_list_2) > 0):
    #         next_move = random.choice (move_list_2)
    #     else:
    #         # He's screwed.
    #         print(f"MOVE {game_state['turn']}: Oh no. ")
    #         next_move = random.choice (move_list_1)
    # else:
    #     print ("Case 3")
    #     print(f"MOVE {game_state['turn']}: I will go out on my own terms!")
    #     next_move = end_it (game_state)


    # food = game_state['board']['food']

    print(f"MOVE {game_state['turn']}: {next_move}")
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


def foresight(game_state: typing.Dict, x, y, px, py, board_width, board_height, fed):
    battlesnakes = game_state['board']['snakes']
    for snake in battlesnakes:
        for bodyCoord in snake['body'][:(fed - 1)]:
            return len(calc_move(game_state, x, y, px, py, board_width, board_height, fed)) > 0


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