import json

def lambda_handler(event, context):
    
    message = event["Records"][0]["body"]
    
    rodada = json.loads(message)
    
    print(rodada)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
