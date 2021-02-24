# ECS deployment

## Configuring the parameters

Please edit the file "paramters.json" with the correct values. You do not have to change the default values unless you want customise it. In addition, you must input the values for:
- MyS3Bucket
- ACM


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


Once you have configured the parameters. In AWS Cli, please enter this command below and make sure the file paths are correct: 

```BASH
aws cloudformation create-stack --stack-name panintelligence /
--template-body file://Panintelligence_Cloudformation_Stack.yaml /
--parameters file://parameters.json / 
--capabilities CAPABILITY_NAMED_IAM

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
