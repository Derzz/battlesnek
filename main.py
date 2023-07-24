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
import aStar
from aStar import *
from flood_fill import *


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
    print("SUCCESSFULLY IMPLEMENTED GRAPH AND NODES")
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    move_area = [
        floodFill(getNextPosition("up", game_state), game_state, arrayify(game_state, not Beeg(game_state))),
        floodFill(getNextPosition("down", game_state), game_state, arrayify(game_state, not Beeg(game_state))),
        floodFill(getNextPosition("left", game_state), game_state, arrayify(game_state, not Beeg(game_state))),
        floodFill(getNextPosition("right", game_state), game_state, arrayify(game_state, not Beeg(game_state))),
    ]

    if len(game_state["board"]["food"]) > 0:
        print("Current position: {}".format(game_state["you"]["head"]))
        print("Closest Food: {}".format(findFood(game_state)))
        move = goto(move_area, findFood(game_state), game_state)

    if is_stuck(move_area, game_state) and max(move_area) != 0:
        if move_area[0] == max(move_area):
            move = "up"
        elif move_area[1] == max(move_area):
            move = "down"
        elif move_area[2] == max(move_area):
            move = "left"
        elif move_area[3] == max(move_area):
            move = "right"

    # Failsafe on
    elif is_stuck(move_area, game_state) and max(move_area) == 0:
        print("Failsafe triggered")

    # Ignores projected heads
    if max(move_area) == 0:
        print("Head prediction off")
        move_area = [
            floodFill(getNextPosition("up", game_state), game_state, arrayify(game_state, False)),
            floodFill(getNextPosition("down", game_state), game_state, arrayify(game_state, False)),
            floodFill(getNextPosition("left", game_state), game_state, arrayify(game_state, False)),
            floodFill(getNextPosition("right", game_state), game_state, arrayify(game_state, False)),
        ]

    if move == "":
        goodMoves = []

        if move_area[0] == max(move_area):
            goodMoves.append("up")

        if move_area[1] == max(move_area):
            goodMoves.append("down")

        if move_area[2] == max(move_area):
            goodMoves.append("left")

        if move_area[3] == max(move_area):
            goodMoves.append("right")

        if len(goodMoves) > 0:
            move = random.choice(goodMoves)

    # End it
    if is_stuck(move_area, game_state) and max(move_area) == 0:
        print(f"MOVE {game_state['turn']}: I will go out on my own terms!")

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

    print(f"MOVE {game_state['turn']}: {move}")
    return {"move": move}

    # Operate A* here
    # if game_state['you']['length'] < 5:
    #     return priorASearch.food(game_state)
    # # Else do flood fill strat
    # else:
    #     print("snake at 5 or more, doing strat")
    #     return {"move": "down"}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
