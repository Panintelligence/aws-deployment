# Cloud formation EC2 deployment

## Launching the Panintelligence dashboard from AWS Marketplace
### Prerequisites
To complete this documentation, we assume you have a Route 53 hosted zone, an ACM certificate that is validated and covers the domain you will be using for the load balancer, an S3 bucket for backups and a key pair to allow you SSH access to the server.

- [Setting up Route 53](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/setting-up-route-53.html)
- [Creating a certificate in ACM](https://docs.aws.amazon.com/acm/latest/userguide/setup.html)
- [Creating a Key Pair](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html)
- [Creating an S3 bucket](https://docs.aws.amazon.com/AmazonS3/latest/gsg/CreatingABucket.html)

## Uploading stack to cloudformation

Once you have the prerequisites done, we can deploy the stack.

### Obtain the panintelligence AMI ID
- Go on to AWS console and search for "AWS marketplace subscriptions":
![marketplace_search.png](/images/marketplace_search.png)

- Inside the AWS marketplace subscriptions, click on "Discover products" on your left and search for "panintelligence": 
![marketplace_ami.png](/images/marketplace_ami.png)

- Select one of the panintelligence products that you wish to use. For this example we will use "Panintelligence BYOL" and select it.

- Click on to "Subscribe" or "Continue to Subscribe" and await to confirm subscription.
![marketplace_sub.png](/cloud/cloudformation/marketplace_sub.png)

- Go back to AWS marketplace subscriptions console in AWS and you should see your panintelligence subscription. Click on to your panintelligence subscription:
![manage_sub.png](/cloud/cloudformation/manage_sub.png)

- Click on to launch instance to your right:
![marketplace.png](/images/marketplace.png)

- Depending on what region you wish to deploy it in, please select the region and below the AMI ID will change. Please copy that AMI ID and keep that safe:
![marketplace_amiid.png](/images/marketplace_amiid.png)

## Configuring the parameters

Please edit the file "paramters.json" with the correct values. You do not have to change the default values unless you want customise it. In addition, you must input the values for:
- MyS3Bucket
- ACM
- AMIID
- keypairvalue


|parameter|description|default value|
|:--|:--|:--|
|VPCCidrBlock| The VPC Cidr block|10.0.0.0/16|
|PublicACidrBlock| Public A Cidr Block|10.0.1.0/24|
|PublicBCidrBlock| Public B Cidr Block|10.0.2.0/24|
|PrivateCidrBlock| Private Cidr Block|10.0.0.0/24|
|AvailabilityZoneA| Availability Zone A|eu-west-1a|
|AvailabilityZoneB| Availability Zone B|eu-west-1b|
|ACMCertArn| ACM Certificate for port 443|No default value|
|MyS3Bucket|The name of the created s3 bucket you wish to upload backups| No default Value|
|AMIID| The AMI ID of the region you wish to use| No default Value| 
|KeyPairName| The key pem name of what you have created| No default value|

Once you have configured the parameters. In AWS Cli, please enter this command below and make sure the file paths are correct: 

```BASH
aws cloudformation create-stack --stack-name panintelligence /
--template-body file://Panintelligence_Cloudformation_Stack.yaml /
--parameters file://parameters.json / 
--capabilities CAPABILITY_NAMED_IAM
```
Once the stack is completed. You will need to obtain the DNS name inside the load balancer.
Please use this command to obtain details:

```BASH
aws elb describe-load-balancers --load-balancer-name Panintelligence
```

## Post launch configuration
**Only do this part if you are hosting your domain on AWS Route 53.**
Finally, we need to create a Route 53 record that aliases to the load balancer.

Navigate to the hosted zone you want to use in Route 53 and create a record set.

Type the subdomain you want to use in the Name field.

Make sure the Type selected is A - IPv4 address and Alias is set to Yes.

In the Alias Target field, start typing the name of the load balancer and select it when it appears.
![alias_target_dropdown.png](/images/alias_target_dropdown.png)

You should now be able to access the dashboard at the domain you configure in the Route 53 record (the DNS entry can sometimes take a little bit to propagate if it doesn't work immediately).
