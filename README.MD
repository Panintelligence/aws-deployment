# How to run Panintelligence AWS Cloudformation stack

- Log into AWS management console
- Go into AWS Cloudshell
- Follow the list of instructions below

## Cloning our Github Repo

Clone our Github project to your cloudshell.

```bash
mkdir panintelligence
cd panintelligence
git clone https://github.com/Panintelligence/aws-deployment.git
cd aws-deployment
```

## Setting the Parameters

> PLEASE NOTE!  your s3 bucket name must be url safe! Also only use DASHBOARDLICENCEKEY if you are inputting your own licence key.

```bash
VPCCIDRBLOCK=10.0.0.0/16
PUBLICZONEACIDRBLOCK=10.0.1.0/24
PUBLICZONEBCIDRBLOCK=10.0.2.0/24
DASHBOARDCIDRBLOCKA=10.0.0.0/24
DASHBOARDCIDRBLOCKB=10.0.5.0/24
AVAILABILITYZONEA=eu-west-1a
AVAILABILITYZONEB=eu-west-1b
RDSUSERNAME= ** your database username **
DBNAME=dashboard
RDSPRIVATEA=10.0.3.0/24
RDSPRIVATEB=10.0.4.0/24
ACMCERTARN= ** your ACM ARN **
ENCRYPTION=true
FILESYSTEMNAME= ** EFS volume name **
AMIID= ** Enter Panintelligence Marketplace AMI here **
KEYPAIRNAME= ** your EC2 keypair name**
DASHBOARDLICENCEKEY= ** Paste your licence key here, make sure it's in line **
REGION=$(aws ec2 describe-availability-zones --output text --query 'AvailabilityZones[0].[RegionName]')
ACCOUNT_ID=$(aws sts get-caller-identity --output text --query '[Account]')
```

### Making your licence key compatible

Please ensure you remove all carriage return line feeds and leading white space from your licence.  It should fit entirely on one line.  If you're running a trial, developer or deploy version of Panintelligence, you will not need to supply this licence here as a licence is provided for you with the AMI.  More documentation can be found at www.panintelligence.com relating to this matter.

## Creating your AWS Panintelligence instance

You will need to add execute to the bash scripts so you can run them in cloudshell.
```bash
chmod +x *.sh
```
This will create a key pair.  If running these scripts from AWS cloudshell, you can download this pem using the download option to the top right dropdown.  To SSH to your instance, you can use SSM (click the connect button in the EC2 interface).  You should keep this key safe in case you lose access via the SSM method.
If you already have a keypair which you will be using, you will not need to use this script to create another.

```bash
aws ec2 create-key-pair --key-name $KEYPAIRNAME --query 'KeyMaterial' --output text > $KEYPAIRNAME.pem
```

This script will build the deployment package for the side load lambda function

```
./build_lambda.sh
```

The first script builds a AWS S3 bucket to upload nested stacks and resources.
``` bash
aws cloudformation create-stack --stack-name PanintelligenceConfig --template-body file://panintelligence_config.yml
./check_stack.sh PanintelligenceConfig
```

We're going to copy lambda zip and the nested stacks to call

```bash
aws s3 cp dist/lambda.zip s3://${ACCOUNT_ID}-panintelligence-configuration
aws s3 cp dist/nested-stacks s3://${ACCOUNT_ID}-panintelligence-configuration --recursive
```

The next script is going to create our side load lambda function which is to help you move themes and images to customise your AWS Panintelligence system.

```bash
aws cloudformation create-stack --stack-name PanintelligenceNestedStack --template-body file://panintelligence_nested_stack.yml --parameters ParameterKey=VPCCidrBlock,ParameterValue=$VPCCIDRBLOCK ParameterKey=PublicZoneACidrBlock,ParameterValue=$PUBLICZONEACIDRBLOCK ParameterKey=PublicZoneBCidrBlock,ParameterValue=$PUBLICZONEBCIDRBLOCK ParameterKey=DashboardCidrBlockZoneA,ParameterValue=$DASHBOARDCIDRBLOCKA ParameterKey=DashboardCidrBlockZoneB,ParameterValue=$DASHBOARDCIDRBLOCKB ParameterKey=DBUserName,ParameterValue=$RDSUSERNAME ParameterKey=DBName,ParameterValue=$DBNAME ParameterKey=RDSPrivateA,ParameterValue=$RDSPRIVATEA ParameterKey=RDSPrivateB,ParameterValue=$RDSPRIVATEB ParameterKey=Encryption,ParameterValue=$ENCRYPTION ParameterKey=FileSystemName,ParameterValue=$FILESYSTEMNAME --capabilities CAPABILITY_NAMED_IAM,CAPABILITY_AUTO_EXPAND
./check_stack.sh PanintelligenceTwo
```

Now we're going to update the stack because of a circular dependency on the s3 bucket and lambda dependency (both need to be created before we can attach the trigger to the s3 bucket.)

```bash
aws cloudformation update-stack --stack-name PanintelligenceTwo --template-body file://panintelligence_nested_stack.yml --parameters ParameterKey=Encryption,ParameterValue=$ENCRYPTION ParameterKey=FileSystemName,ParameterValue=$FILESYSTEMNAME --capabilities CAPABILITY_NAMED_IAM
./check_stack_update.sh PanintelligenceTwo
```

We need to create some default themes for s3.  If you want to create your own, you can find instructions for this at www.panintelligence.com

```bash
aws s3 cp resources/themes s3://panintelligence---${REGION}--${ACCOUNT_ID}/themes --recursive
aws s3 cp resources/images s3://panintelligence---${REGION}--${ACCOUNT_ID}/images --recursive
```

In the next step, we're going to create an autoscaling group and a launch configuration which will run a specified (default 1) number of Panintelligence instances inside your newly created infrastructure.
### If you are using a licence key, please use the script below: 

```bash
aws cloudformation create-stack --stack-name PanintelligenceThree --template-body file://infrastructure_setup_three.yml --parameters ParameterKey=AMIID,ParameterValue=$AMIID ParameterKey=KeyPairName,ParameterValue=$KEYPAIRNAME ParameterKey=DashboardLicenceKey,ParameterValue="${DASHBOARDLICENCEKEY}" --capabilities CAPABILITY_NAMED_IAM
./check_stack.sh PanintelligenceThree
```
### If you are not using a licence key, please use the script below:
```bash
aws cloudformation create-stack --stack-name PanintelligenceThree --template-body file://infrastructure_setup_three_wol.yml --parameters ParameterKey=AMIID,ParameterValue=$AMIID ParameterKey=KeyPairName,ParameterValue=$KEYPAIRNAME --capabilities CAPABILITY_NAMED_IAM
./check_stack.sh PanintelligenceThree
```

## How to Clean up your AWS Marketplace Panintelligence 
Please empty the S3 buckets before deleting the stacks. Beaware you are deleting the files inside the bucket, please make sure you have a backup of files.
```bash
aws s3 rm s3://panintelligence---${REGION}--${ACCOUNT_ID} --recursive
aws s3 rm s3://${S3BUCKETNAME} --recursive
```

Please ensure the stacks are deleted prior to running the next.  Please run these sequentially to ensure there's no additional hanging resources.

```bash
aws cloudformation delete-stack --stack-name PanintelligenceThree
aws cloudformation delete-stack --stack-name PanintelligenceTwo
aws cloudformation delete-stack --stack-name PanintelligenceOne
```






