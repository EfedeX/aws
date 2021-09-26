import boto3
aws_access_key_id = 'aws_access_key_id'
aws_secret_access_key = 'aws_secret_access_key'

#Funcion que obtiene el nombre de la ultima imagen subida al bucket
def get_bucket_name():
    s3 = boto3.client('s3', region_name='us-east-1', aws_access_key_id=aws_access_key_id, 
                  aws_secret_access_key=aws_secret_access_key)
    response = s3.list_objects(Bucket='compress-images6662')
    values = []
    for value in response['Contents']:
        values.append(value['LastModified'])

    last_photo = max(values)
    for key in response['Contents']:
        if key['LastModified'] == last_photo:
            photo_name = key['Key']
            break
            
    return photo_name
    
def detect_labels(photo, bucket):

    client=boto3.client('rekognition', region_name='us-east-1', aws_access_key_id=aws_access_key_id, 
                  aws_secret_access_key=aws_secret_access_key)

    response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}},
        MaxLabels=15, MinConfidence=70)

    print('Detected labels for ' + photo) 
    print()   
    for label in response['Labels']:
        print ("Label: " + label['Name'])
        print ("Confidence: " + str(label['Confidence']))
        print ("Instances:")
        for instance in label['Instances']:
            print ("  Bounding box")
            print ("    Top: " + str(instance['BoundingBox']['Top']))
            print ("    Left: " + str(instance['BoundingBox']['Left']))
            print ("    Width: " +  str(instance['BoundingBox']['Width']))
            print ("    Height: " +  str(instance['BoundingBox']['Height']))
            print ("  Confidence: " + str(instance['Confidence']))
            print()

        print ("Parents:")
        for parent in label['Parents']:
            print ("   " + parent['Name'])
        print ("----------")
        print ()
    #return len(response['Labels'])
    return response


def main():
    photo=get_bucket_name()
    bucket='compress-images6662'
    label_count=detect_labels(photo, bucket)
    print("Labels detected: " + str(label_count))


if __name__ == "__main__":
    main()
