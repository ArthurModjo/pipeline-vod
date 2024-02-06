import boto3
import uuid
from botocore.exceptions import NoCredentialsError

working_dir = '/processing'

def upload_to_s3(file, bucket_name):
    """Upload a file to an S3 bucket."""
    # Créer une session S3
    session = boto3.Session(
        aws_access_key_id='AKIAQSK4UGYQYQVISOV7',
        aws_secret_access_key='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',
        region_name='eu-north-1'
    )

    # Créer un client S3
    s3 = session.client('s3')

    #get the file name
    file_name = file.split("/")[-1]

    try:
        s3.upload_file(file, bucket_name, file_name)
        print(f"File {file} uploaded to {bucket_name}/{file_name}")
        return True
    except FileNotFoundError:
        print(f"The file {file} was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

def save_to_dynamodb(file_dict, bucket_name):
    """Save file details to DynamoDB."""
    session = boto3.Session(
        aws_access_key_id='AKIAQSK4UGYQYQVISOV7',
        aws_secret_access_key='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',
        region_name='eu-north-1'
    )

    dynamodb = session.client('dynamodb')

    item = {
        'fileID': {"S": file_dict['video']},
        'langue': {"S": file_dict['langue']},
        'subtitles': {"S": file_dict['subtitles']},
        'animal': {"S": file_dict['animal']},
        'bucket_name': {"S": bucket_name},
        
    }

    response = dynamodb.put_item(TableName="piplelineVodDB",Item=item)
    print(f"File details saved to DynamoDB: {response}")

def process_files(file_dict, bucket_name):
    """Process a list of files, upload to S3, and save details to DynamoDB."""
    list_files = []
    for key, value in file_dict.items():
        list_files.append(value)
    for file in list_files:
        file_id = str(uuid.uuid4())
        upload_to_s3(working_dir+"/"+file, bucket_name)
        save_to_dynamodb(file_dict,bucket_name)

