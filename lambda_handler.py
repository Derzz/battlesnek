import json
import os
import traceback
import main


def lambda_handler(event, context):
    body = {}
    try:
        # If GET and path is /
        if event['path'] == "/" and event['httpMethod'] == "GET":
            body.update(main.info())

        # if POST
        elif event['httpMethod'] == 'POST':
            # if /start
            if event['path'] == "/start":
                game_state = json.loads(event['body'])
                main.start(game_state)

            # if move
            elif event['path'] == "/move":
                game_state = json.loads(event['body'])
                body = main.move(game_state)

            # if end
            elif event['path'] == "/end":
                game_state = json.loads(event['body'])
                main.end(game_state)

        # if command not recognized
        else:
            raise Exception("Unknown Command")

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(body)
        }

    # if unknown command
    except Exception as e:
        json_region = os.environ['AWS_REGION']
        return {
            "statusCode": 404,
            "headers": {
                "Content-Type": "application/json"
            },
            'body': json.dumps({
                "error": str(e),
                "errorTraceback": traceback.format_exc(),
                "Region": json_region,
                "Path": event.get('path', 'unknown'),
                "event": event,
            })
        }