import json;
import main


def lambda_handler(event, context):
    body = ""
    if event['path'] == "/" and event['httpMethod'] == "GET":
        body = json.dumps(main.info())

    elif event['httpMethod'] == 'POST':
        if event['path'] == "/start":
            game_state = event['body']
            main.start(json.loads(game_state))
            body = "ok"
        elif event['path'] == "/move":
            game_state = event['body']
            body = json.dumps(main.move(json.loads(game_state)))
        elif event['path'] == "/end":
            game_state = event['body']
            main.end(json.loads(game_state))
            body = "ok"

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": body
    }
