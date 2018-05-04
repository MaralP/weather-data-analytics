import time as t
import boto3
import json
import decimal
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
import sys

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

dynamodb = boto3.resource('dynamodb',region_name = 'us-east-2')

table = dynamodb.Table('CurrentWeather')

cityId = input('City Id:')#6173331,6085772

try:

    response = table.query(
        KeyConditionExpression=Key('CityId').eq(int(cityId))
    )

except ClientError as e:
    print(e.response['Error']['Message'])
else:

    items = response['Items']
    print("GetItem succeeded.")
    #print(json.dumps(item, indent=4, cls=DecimalEncoder))

    currentdatetime = t.strftime("%Y%m%d-%H%M%S")
    with open('E:\\2017\\MyProject\\Temp\\data'+currentdatetime+'.txt', 'w') as outfile:
        json.dump(items, outfile, indent=4,cls=DecimalEncoder)
