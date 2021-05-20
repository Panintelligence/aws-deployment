# How to run Panintelligence AWS Cloudformation stack

- Log into AWS management console
- Go into AWS Cloudshell


## Prerequisite 

## Git clone
```BASH
mkdir panintelligence
cd panintelligence
git clone https://github.com/Panintelligence/aws-deployment.git
cd aws-deployment
```


## Setting the parameters:
### Don't make your bucket with hyphens
```BASH
VPCCIDRBLOCK=10.0.0.0/16
PUBLICZONEACIDRBLOCK=10.0.1.0/24
PUBLICZONEBCIDRBLOCK=10.0.2.0/24
DASHBOARDCIDRBLOCK=10.0.0.0/24
AVAILABILITYZONEA=eu-west-1a
AVAILABILITYZONEB=eu-west-1b
RDSUSERNAME=dashboard
RDSPASSWORD=5up3r53cur3P455w0rd!
DBNAME=dashboard
RDSPRIVATEA=10.0.3.0/24
RDSPRIVATEB=10.0.4.0/24
ACMCERTARN=<paste your ACM ARN here>
S3BUCKETNAME=<Enter bucket name so you can upload lambda zip>
ENCRYPTION=true
FILESYSTEMNAME=<Give a name for your EFS>
AMIID=<Enter Panintelligence AMI here>
KEYPAIRNAME=<Enter your Key pair name here>
DASHBOARDLICENCEKEY=<Paste your licence key here, make sure it's in line>
REGION=$(aws ec2 describe-availability-zones --output text --query 'AvailabilityZones[0].[RegionName]')
ACCOUNT_ID=$(aws sts get-caller-identity --output text --query '[Account]')
```
## Run these commands 

- Create the keypair
This is an example of creating a keypair that you can use. 
```BASH
aws ec2 create-key-pair --key-name $KEYPAIRNAME --query 'KeyMaterial' --output text > $KEYPAIRNAME.pem
```

- build lambda script to zip lambda function
```
./build_lambda.sh
```

-  This script builds the infrastructure of VPC and networking side
``` BASH
aws cloudformation create-stack --stack-name PanintelligenceOne --template-body file://infrastructure_setup_one.yaml --parameters ParameterKey=VPCCidrBlock,ParameterValue=$VPCCIDRBLOCK ParameterKey=PublicZoneACidrBlock,ParameterValue=$PUBLICZONEACIDRBLOCK ParameterKey=PublicZoneBCidrBlock,ParameterValue=$PUBLICZONEBCIDRBLOCK ParameterKey=DashboardCidrBlock,ParameterValue=$DASHBOARDCIDRBLOCK ParameterKey=AvailabilityZoneA,ParameterValue=$AVAILABILITYZONEA ParameterKey=AvailabilityZoneB,ParameterValue=$AVAILABILITYZONEB ParameterKey=RDSUsername,ParameterValue=$RDSUSERNAME ParameterKey=RDSPassword,ParameterValue=$RDSPASSWORD ParameterKey=DBName,ParameterValue=$DBNAME ParameterKey=RDSPrivateA,ParameterValue=$RDSPRIVATEA ParameterKey=RDSPrivateB,ParameterValue=$RDSPRIVATEB ParameterKey=ACMCertArn,ParameterValue=$ACMCERTARN ParameterKey=S3BucketName,ParameterValue=$S3BUCKETNAME --capabilities CAPABILITY_NAMED_IAM
```

Wait until the stack is built (eta 2 minutes), check the status with this command and wait for "CREATE_COMPLETE":
```BASH
./check_stack.sh PanintelligenceOne
```

-  The S3 bucket that you have created, copy the lambda.zip to that bucket

```BASH
aws s3 cp dist/lambda.zip s3://{$S3BUCKETNAME}
```

-  Next onto the lambda function deployment

```BASH
aws cloudformation create-stack --stack-name PanintelligenceTwo --template-body file://infrastructure_setup_two.yml --parameters ParameterKey=Encryption,ParameterValue=$ENCRYPTION ParameterKey=FileSystemName,ParameterValue=$FILESYSTEMNAME --capabilities CAPABILITY_NAMED_IAM
```
Wait until the stack is built (eta 2 minutes), check the status with this command and wait for "CREATE_COMPLETE":
```BASH
./check_stack.sh PanintelligenceTwo
```
We will need to update the stack for PanintelligenceTwo:

```BASH
aws cloudformation update-stack --stack-name PanintelligenceTwo --template-body file://infrastructure_setup_two_updated.yml --parameters ParameterKey=Encryption,ParameterValue=$ENCRYPTION ParameterKey=FileSystemName,ParameterValue=$FILESYSTEMNAME --capabilities CAPABILITY_NAMED_IAM
```
Wait until the stack is built (eta 2 minutes), check the status with this command and wait for "CREATE_COMPLETE":
```BASH
./check_stack.sh PanintelligenceTwo
```
 Now upload the themes and images to s3 

```BASH
cd /resources/
```
```BASH
aws s3 cp themes s3://panintelligence---${REGION}--${ACCOUNT_ID}/themes --recursive
```
```BASH
aws s3 cp images s3://panintelligence---${REGION}--${ACCOUNT_ID}/images --recursive
```

-  We will need to deploy the AMI. As there is a circular dependency we will need to update it afterwards. 

```BASH
aws cloudformation create-stack --stack-name PanintelligenceThree --template-body file://infrastructure_setup_three.yml --parameters ParameterKey=AMIID,ParameterValue=$AMIID ParameterKey=KeyPairName,ParameterValue=$KEYPAIRNAME ParameterKey=DashboardLicenceKey,ParameterValue=$DASHBOARDLICENCEKEY --capabilities CAPABILITY_NAMED_IAM
```
Wait until the stack is built (eta 2 minutes), check the status with this command and wait for "CREATE_COMPLETE":
```BASH
./check_stack.sh PanintelligenceThree
```

## How to tear down your cloudformation stack safely: 

```
aws cloudformation delete-stack --stack-name PanintelligenceThree
```

```
aws cloudformation delete-stack --stack-name PanintelligenceTwo
```

```
aws cloudformation delete-stack --stack-name PanintelligenceOne
```






