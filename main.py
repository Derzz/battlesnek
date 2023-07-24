# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#

# This snake will focus on using the A* algorithm to find the nearest pellet to it.

import json
import os
import random
import typing
import aStar
from aStar import *


def info():
    print ("INFO")
    return {
        "apiversion": "1",
        "author": "pixelsnek",
        "color": "#811313",
        "head": "mask",
        "tail": "snowflake",
    }


def index():
    return "From the ashes I rise."


def start (game_state):
    """
    Called every time a new Battlesnake game starts and snek is in it.
    Response will control how snek is displayed.
    """
    print ("GAME START")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
# def move(game_state: typing.Dict) -> typing.Dict:
#     # Operate A* here
#     if game_state['you']['length'] < 5:
#         return priorASearch.food(game_state)
#     # Else do flood fill strat
#     else:
#         print("snake at 5 or more, doing strat")
#         return {"move": "down"}


def move (game_state):
    """
    Called when the Battlesnake Engine needs to know your next move.
    The data parameter will contain information about the board.
    Your response must include your move of up, down, left, or right.
    """
    game_state
    move = ""
    up_area = floodFill (getNextPosition ("up", game_state), game_state, arrayify (game_state, not Beeg (game_state)))
    down_area = floodFill (getNextPosition ("down", game_state), game_state, arrayify (game_state, not Beeg (game_state)))
    right_area = floodFill (getNextPosition ("right", game_state), game_state, arrayify (game_state, not Beeg (game_state)))
    left_area = floodFill (getNextPosition ("left", game_state),  game_state, arrayify (game_state, not Beeg (game_state)))
    move_area = [up_area, down_area, right_area, left_area]

    if len (game_state["board"]["food"]) > 0:
        print ("Current position: {}".format (game_state["you"]["head"]))
        print ("Closest Food: {}".format (findFood (game_state)))
        move = goto (move_area, findFood (game_state), game_state)

    if is_stuck (move_area, game_state) and max (move_area) != 0:
        if up_area == max (move_area):
            move = "up"
        elif down_area == max (move_area):
            move = "down"
        elif left_area == max (move_area):
            move = "left"
        elif right_area == max (move_area):
            move = "right"

    # Failsafe on
    if is_stuck (move_area, game_state) and max (move_area) == 0:
        print ("Failsafe triggered")

    # Ignores projected heads
    if max (move_area) == 0:
        print ("Head prediction off")
        up_area = floodFill (getNextPosition ("up", game_state), game_state, arrayify (game_state, False))
        down_area = floodFill (getNextPosition ("down", game_state), game_state, arrayify (game_state, False))
        right_area = floodFill (getNextPosition ("right", game_state), game_state, arrayify (game_state, False))
        left_area = floodFill (getNextPosition ("left", game_state),  game_state, arrayify (game_state, False))
        move_area = [up_area, down_area, right_area, left_area]

    if move == "":
        goodMoves = []

        if up_area == max (move_area):
            goodMoves.append ("up")

        if down_area == max (move_area):
            goodMoves.append ("down")

        if left_area == max (move_area):
            goodMoves.append ("left")

        if right_area == max (move_area):
            goodMoves.append ("right")

        if (len (goodMoves) > 0):
            move = random.choice (goodMoves)

    # End it
    if is_stuck (move_area, game_state) and max (move_area) == 0:
        print (f"MOVE {game_state['turn']}: I will go out on my own terms!")

        if game_state["you"]["body"][1]["x"] < game_state["you"]["body"][0]["x"]:  # Neck is left of head, move left
            move = "left"
        elif game_state["you"]["body"][1]["x"] > game_state["you"]["body"][0]["x"]:  # Neck is right of head, move right
            move = "right"
        elif game_state["you"]["body"][1]["y"] < game_state["you"]["body"][0]["y"]:  # Neck is below head, move down
            move = "down"
        elif game_state["you"]["body"][1]["y"] > game_state["you"]["body"][0]["y"]:  # Neck is above head, move up
            move = "up"
        else:
            move = "down"

    print (f"MOVE {game_state['turn']}: {move}")
    return {"move": move}


def end (game_state):
    """
    Called every time a game with your snake in it ends.
    """
    print ("GAME OVER")


def is_stuck (move_area, data):
    body_length = len (data["you"]["body"])

    if max (move_area) < body_length:
        return True
    return False


def getNextPosition (move, data):
    """
    returns next position depending on which inputted
    """
    nextPos = {"x": data["you"]["head"]['x'], "y": data["you"]["head"]['y']}

    if move == 'up':
        nextPos["y"] = nextPos["y"] + 1
    elif move == 'down':
        nextPos["y"] = nextPos["y"] - 1
    elif move == 'right':
        nextPos["x"] = nextPos["x"] + 1
    elif move == 'left' :
        nextPos["x"] = nextPos["x"] - 1
    return nextPos


#if cords are not within the board, return false else return true
def is_cords_in_board (x, y, height, width):
    if x < 0 or x > width - 1:
        return False
    
    if y < 0 or y > height - 1:
        return False
    return True


def is_occupied (x, y, dataArray):
    game_width = len (dataArray)
    game_height = len (dataArray[0])

    if not is_cords_in_board (x, y, game_height, game_width):
        return True
    elif dataArray[x][y] == 1:
        return True
    return False


def floodFill (pos, data, dataArray):
    """
    Check the remaining space of a projected move
    Returns free space
    """
    count = 0

    if is_occupied (pos["x"], pos["y"], dataArray):
        return count
    
    # mark node as visited
    dataArray[pos["x"]][pos["y"]] = 1

    count += 1
    count += floodFill ({"x": pos["x"], "y": pos["y"] - 1}, data, dataArray)
    count += floodFill ({"x": pos["x"], "y": pos["y"] + 1}, data, dataArray)
    count += floodFill ({"x": pos["x"] - 1, "y": pos["y"]}, data, dataArray)
    count += floodFill ({"x": pos["x"] + 1, "y": pos["y"]}, data, dataArray)
    return count


def arrayify (data, ghost_heads: bool):
    height = data["board"]["height"]
    width = data["board"]["width"]

    array = [[0] * height for i in range (width)]
    snakes = data["board"]["snakes"]

    for snake in snakes:
        if snake["health"] == 100:
            for body_part in snake["body"]:
                array[body_part["x"]][body_part["y"]] = 1
        else:
            for body_part in snake["body"][: - 1]:
                array[body_part["x"]][body_part["y"]] = 1
    if ghost_heads:
        for snake in snakes:
            if snake["id"] == data["you"]["id"]:
                continue
            head_x = snake["head"]["x"]
            head_y = snake["head"]["y"]

            if is_cords_in_board (head_x - 1, head_y, height, width):
                array[head_x - 1][head_y] = 1

            if is_cords_in_board (head_x + 1, head_y, height, width):
                array[head_x + 1][head_y] = 1

            if is_cords_in_board (head_x, head_y - 1, height, width):
                array[head_x][head_y - 1] = 1

            if is_cords_in_board (head_x, head_y + 1, height, width):
                array[head_x][head_y + 1] = 1
    return array


def Beeg (data):
    """
    Returns true if snek is the longest snake on the board, otherwise returns false
    """
    myLength = len (data["you"]["body"])

    for i in data["board"]["snakes"]:
        if i["id"] != data["you"]["id"] and myLength <= len (i["body"]):
            return False
    return True


def findFood (data):
    """
    Locates closest food to snake
    """
    x = data["you"]["head"]["x"]
    y = data["you"]["head"]["y"]
    food = data["board"]["food"]
    closest_food = data["board"]["food"][0]

    for food in data["board"]["food"]:
        distance_x = abs (x - food["x"])
        distance_y = abs (y - food["y"])
        delta_distance = distance_x + distance_y
        current_closest_distance = abs (x - closest_food["x"]) + abs (y - closest_food["y"])

        if delta_distance < current_closest_distance:
            closest_food = food
    return closest_food


def goto (move_area, pos, data):
    """
    Sends snek to position
    """
    body_length = len (data["you"]["body"])
    my_head_x = data["you"]["head"]["x"]
    my_head_y = data["you"]["head"]["y"]
    distance_x = my_head_x - pos["x"]
    distance_y = my_head_y - pos["y"]

    move_x = ""
    move_x_area = 0

    if distance_x > 0:
        move_x = "left"
        move_x_area = move_area[3]
    elif distance_x < 0:
        move_x = "right"
        move_x_area = move_area[2]
    move_y = ""
    move_y_area = 0

    if distance_y > 0:
        move_y = "down"
        move_y_area = move_area[1]
    elif distance_y < 0:
        move_y = "up"  
        move_y_area = move_area[0]

    if move_x_area < body_length:
        move_x_area = 0
        move_x = ""

    if move_y_area < body_length:
        move_y_area = 0
        move_y = ""

    # If no valid moves, return empty str; If only one is valid, return it; If both are valid choose move with most remaining area
    if move_y == "" and move_x == "":
        return ""
    elif move_y == "":
        return move_x
    elif move_x == "":
        return move_y
    elif move_x_area > move_y_area:
        return move_x
    elif move_y_area > move_x_area:
        return move_y
    else:
        return random.choice ([move_x, move_y])

 
# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server ({"info": info, "start": start, "move": move, "end": end}, 8001)
