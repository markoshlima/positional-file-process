import json
import boto3

#instancia o client
client = boto3.client('glue')

#jobname
glueJobName = "SoccerJob"

def lambda_handler(event, context):
    
    print('INICIO ')
    
    #monta URI do arquivo S3
    bucket = event['Records'][0]['s3']['bucket']['name']
    filename = event['Records'][0]['s3']['object']['key']
    file= 's3://'+bucket+'/'+filename
    
    #chama o JOB
    response = client.start_job_run(
             JobName = glueJobName,
             Arguments = {'--file':file})
             
    print('## INICIO GLUE JOB: ' + glueJobName)
    print('## FILE: ' + file)
    print('## GLUE JOB RUN ID: ' + response['JobRunId'])
    return response

