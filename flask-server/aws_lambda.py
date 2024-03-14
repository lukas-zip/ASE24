import boto3
import json

# Create IAM client
iam_client = boto3.client('iam', endpoint_url="http://localhost:4566", aws_access_key_id="test", aws_secret_access_key="test", region_name="us-east-1")
data = json.load("/policy.json")
json.dumps(data)
response = iam_client.create_role(
    RoleName='iam_role',
    AssumeRolePolicyDocument= data,
    Description='iam_role',
)

# Lambda function 

# Initialize client
lambda_client = boto3.client('lambda', endpoint_url="http://localhost:4566", aws_access_key_id="test", aws_secret_access_key="test", region_name="us-east-1")

# Create lambda function
response = lambda_client.create_function(FunctionName = 'function_name', Description = "frist_function", Role = None, Runtime = "python3.11", Handler = 'handler_name', Code={"ZipFile": 'deployment_package'}, Publish=True)

#Invoce lambda function
response = lambda_client.invoke(FunctionName='function_name')