import json;
import os

import main


def lambda_handler(event, context):
    body = ""
    try:
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
        else:
            raise Exception("Unknown Command")

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": body
        }
    except:
        json_region = os.environ['AWS_REGION']
        return {
            "statusCode": 404,
            "headers": {
                "Content-Type": "application/json"
            },
            'body': json.dumps({
                "Region ": json_region
            })
        }


