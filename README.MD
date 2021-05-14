# How to run Panintelligence AWS Cloudformation stack

- Log into AWS management console
- Go into AWS Cloudshell
- Sign into git 
- git clone this project


## Prerequisite 
Edit the parameters for each json file to pass the value into the yaml scripts. Some values are set to default.

## Create the key pair

This is an example of creating a keypair that you can use
```BASH
aws ec2 create-key-pair --key-name Panintelligence --query 'KeyMaterial' --output text > Panintelligence.pem
chmod 400 MyKeyPair.pem
```

## Setting the parameters:
infrastructure_setup_one:
```BASH
VPCCIDRBLOCK=10.0.0.0/16
PUBLICZONEACIDRBLOCK=10.0.1.0/24
PUBLICZONEBCIDRBLOCK=10.0.1.0/24
DASHBOARDCIDRBLOCK=10.0.0.0/24
AVAILABILITYZONEA=eu-west-1a
AVAILABILITYZONEB=eu-west-1b
RDSUSERNAME=dashboard
RDSPASSWORD=5up3r53cur3P455w0rd!
DBNAME=dashboard
RDSPUBLICA=10.0.3.0/24
RDSPUBLICB=10.0.3.0/24
ACMCERTARN=<paste your ACM ARN here>
```
S3_creation:
```
S3BUCKETNAME=<Enter bucket name so you can upload lambda zip>
```

Infrastructure set up two: 
```BASH
ENCRYPTION=true
FILESYSTEMNAME=<Give a name for your EFS>
PERFORMANCEMODE=generalPurpose
S3LAMBDABUCKET=<Enter the S3 bucket name that you have created for lambda zip>
```
Infrastructure_setup_three: 

```BASH
AMIID=<Enter Panintelligence AMI here>
KEYPAIRNAME=<Enter your Key pair name here>
DASHBOARDLICENCEKEY=<Paste your licence key here, make sure it's in line>
```
## Run these commands 

- 1) This script builds the infrastructure of VPC and networking side
``` BASH
aws cloudformation create-stack --stack-name panintelligence_setup_one --template-body file://infrastructure_setup_one.yaml --parameters ParameterKey=VPCCidrBlock,ParameterValue=$VPCCIDRBLOCK ParameterKey=PublicZoneACidrBlock,ParameterValue=$PUBLICZONEACIDRBLOCK ParameterKey=PublicZoneBCidrBlock,ParameterValue=$PUBLICZONEBCIDRBLOCK ParameterKey=DASHBOARDCIDRBLOCK,ParameterValue=$DashboardCidrBlock ParameterKey=AvailabilityZoneA,ParameterValue=$AVAILABILITYZONEA ParameterKey=AvailabilityZoneB,ParameterValue=$AVAILABILITYZONEB ParameterKey=RDSUsername,ParameterValue=$RDSUSERNAME ParameterKey=RDSPassword,ParameterValue=$RDSPASSWORD ParameterKey=DBName,ParameterValue=$DBNAME ParameterKey=RDSPublicA,ParameterValue=$RDSPUBLICA ParameterKey=RDSPublicB,ParameterValue=$RDSPUBLICB ParameterKey=ACMCertArn,ParameterValue=$ACMCERTARN --capabilities CAPABILITY_NAMED_IAM
```

- 2) Create an s3 bucket to upload the lambda function:

```BASH
aws cloudformation create-stack --stack-name panintelligence_setup_s3 --template-body file://s3_creation.yaml --parameters ParameterKey=S3BucketName,ParameterValue=$S3BUCKETNAME --capabilities CAPABILITY_NAMED_IAM
```
- 3) The S3 bucket that you have created, copy the lambda.zip to that bucket

```BASH
aws s3 cp lambda.zip s3://{$S3BUCKETNAME}
```

- 4) Next onto the lambda function deployment

```BASH
aws cloudformation create-stack --stack-name panintelligence_setup_two --template-body file://infrastructure_setup_two.yml --parameters ParameterKey=Encryption,ParameterValue=$ENCRYPTION ParameterKey=FileSystemName,ParameterValue=$FILESYSTEMNAME ParameterKey=PerformanceMode,ParameterValue=$PERFORMANCEMODE ParameterKey=S3lambdabucket,ParameterValue=$S3LAMBDABUCKET --capabilities CAPABILITY_NAMED_IAM
```

- 5) We will need to deploy the AMI. As there is a circular dependency we will need to update it afterwards. 
```BASH
aws cloudformation create-stack --stack-name panintelligence_setup_three --template-body file://infrastructure_setup_three.yml --parameters ParameterKey=AMIID,ParameterValue=$AMIID ParameterKey=KeyPairName,ParameterValue=$KEYPAIRNAME ParameterKey=DashboardLicenceKey,ParameterValue=$DASHBOARDLICENCEKEY --capabilities CAPABILITY_NAMED_IAM
```
Once this is done, please update it with this script:
```BASH
aws cloudformation update-stack --stack-name panintelligence_setup_three --template-body file://infrastructure_setup_three_update.yml --parameters ParameterKey=AMIID,ParameterValue=$AMIID ParameterKey=KeyPairName,ParameterValue=$KEYPAIRNAME ParameterKey=DashboardLicenceKey,ParameterValue=$DASHBOARDLICENCEKEY --capabilities CAPABILITY_NAMED_IAM
```

6) Now upload the themes and images to s3 that was created in step 5.
it should look like "panintelligence-{aws-region}-{aws-accountid}
```BASH
aws s3 ls
```
```BASH
cd /resources/
```
```BASH
aws s3 cp themes s3://{BUCKET_NAME_HERE]
```
```BASH
aws s3 cp images s3://{BUCKET_NAME_HERE]
```






