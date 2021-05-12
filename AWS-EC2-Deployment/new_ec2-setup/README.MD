# How to run Panintelligence AWS Cloudformation stack

- Log into AWS management console
- Go into AWS Cloudshell
- Sign into git 
- git clone this project


## Prerequisite 
Edit the parameters for each json file to pass the value into the yaml scripts. Some values are set to default.

## Run these commands 

- 1) This script builds the infrastructure of VPC and networking side
``` BASH
aws cloudformation create-stack --stack-name panintelligence_setup_one --template-body file://infrastructure_setup_one.yaml --parameters file://setup_one_parameters.json --capabilities CAPABILITY_NAMED_IAM
```

- 2) Create an s3 bucket to upload the lambda function:

```BASH
aws cloudformation create-stack --stack-name panintelligence_setup_s3 --template-body file://s3_creation.yaml --parameters file://s3_parameters.json --capabilities CAPABILITY_NAMED_IAM
```
- 3) The S3 bucket that you have created, copy the lambda.zip to that bucket

```BASH
aws s3 cp lambda.zip s3://{BUCKET_NAME_HERE]
```

- 4) Next onto the lambda function deployment

```BASH
aws cloudformation create-stack --stack-name panintelligence_setup_two --template-body file://infrastructure_setup_two.yml --parameters file://setup_two_parameters.json --capabilities CAPABILITY_NAMED_IAM
```

- 5) We will need to deploy the AMI. As there is a circular dependency we will need to update it afterwards. 
```BASH
aws cloudformation create-stack --stack-name panintelligence_setup_three --template-body file://infrastructure_setup_three.yml --parameters file://setup_three_parameters.json --capabilities CAPABILITY_NAMED_IAM
```
Once this is done, please update it with this script:
```BASH
aws cloudformation update-stack --stack-name panintelligence_setup_three --template-body file://infrastructure_setup_three_update.yml --parameters file://setup_three_parameters.json --capabilities CAPABILITY_NAMED_IAM
```



