import json
import boto3

dynamodbTableName = "Task"
dynamodb=boto3.resource('dynamodb')
table=dynamodb.Table(dynamodbTableName)

def lambda_handler(event, context):
    #get apigateway method request
    method = event['httpMethod']
    if method == 'GET':
        return get(event, context)
    elif method == 'POST':
        return post(event, context)
    elif method == 'PUT':
        return put(event, context)
    elif method == 'DELETE':
        return delete(event, context)
    else:
        return {
            'statusCode': 405,
            'body': json.dumps('Method not allowed')
        }

def get(event):
    #get all tasks
    response = table.scan()
    return {
        'statusCode': 200,
        'body': json.dumps(response['Items'])
    }

def delete(event, context):
    #delete task by id
    requestBody = json.loads(event["body"])
    id = requestBody["id"]
    response = table.delete_item(
        Key={
            'id': id
        }
    )
    return {
        'statusCode': 200,
        'body': json.dumps('Task deleted successfully')
    }

def post(event, context):
    #create new task
    requestBody = json.loads(event["body"])
    id = requestBody["id"]
    name = requestBody["name"]
    description = requestBody["description"]
    response = table.put_item(
       Item={
            'id': id,
            'name': name,
            'description': description
        }
    )
    return {
        'statusCode': 200,
        'body': json.dumps('Task created successfully')
    }

def put(event, context):
    #update task
    requestBody = json.loads(event["body"])
    id = requestBody["id"]
    name = requestBody["name"]
    description = requestBody["description"]
    response = table.update_item(
        Key={
            'id': id
        },
        UpdateExpression="set #n = :n, description = :d",
        ExpressionAttributeValues={
            ':n': name,
            ':d': description
        },
        ExpressionAttributeNames={
            "#n": "name"
        },
        ReturnValues="UPDATED_NEW"
    )
    return {
        'statusCode': 200,
        'body': json.dumps('Task updated successfully')
    }