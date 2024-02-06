import boto3

# Créer une session S3
session = boto3.Session(
    aws_access_key_id='AKIAQSK4UGYQYQVISOV7',
    aws_secret_access_key='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',
    region_name='eu-north-1'
)

# Créer un client S3
s3 = session.client('s3')

# Créer un client DynamoDB
dynamodb = session.client('dynamodb')

# Envoyer un fichier vers un bucket S3
bucket_name = 'pipeline-vod-group-kdavid'
file_path = '/home/bad/LAB/pipeline-vod/processing/animaux.mp4'
object_key = 'animaux.mp4'

with open(file_path, 'rb') as file:
    s3.upload_fileobj(file, bucket_name, object_key)

# Enregistrer la donnée dans DynamoDB
table_name = 'piplelineVodDB'
data = {
    'fileID': {
        'S': 'animaux.txt'
    },
    'file_path': {
        'S': file_path
    },
    'bucket_name': {
        'S': bucket_name
    },

    'object_key': {
        'S': object_key
    }
}

if (dynamodb.put_item(TableName=table_name, Item=data)) :
    
    print("Fichier envoyé avec succès vers S3 et enregistré dans DynamoDB.")
else :
    print("Erreur lors de l'envoi du fichier vers S3 et l'enregistrement dans DynamoDB.")


