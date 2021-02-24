# ECS deployment

## Configuring the parameters

Please edit the file "paramters.json" with the correct values. You do not have to change the default values unless you want customise it. In addition, you must input the values for:
- Licence
- ACM
- DockerUser
- DockerPass

|parameter|description|default value|
|:--|:--|:--|
|VPCCidrBlock| The VPC Cidr block|10.0.0.0/16|
|PublicACidrBlock| Public A Cidr Block|10.0.1.0/24|
|Licence| The Licence key for the Panintelligence dashboard|No default value|
|PublicBCidrBlock| Public B Cidr Block|10.0.2.0/24|
|PrivateCidrBlock| Private Cidr Block|10.0.0.0/24|
|RDSPublicA| Public A Cidr Block for database|10.0.3.0/24|
|RDSPublicB| Public B Cidr Block for database|10.0.4.0/24|
|AvailabilityZoneA| Availability Zone A|eu-west-1a|
|AvailabilityZoneB| Availability Zone B|eu-west-1b|
|RDSUsername| Username of the RDS|dashboard|
|RDSPassword| Password for the RDS|dashboard12|
|RDSEngine| The Engine of the RDS|mariadb|
|DBInstanceIdentifier| Instance name for the RDS|dashboard|
|DBInstanceClass| Size of RDS|db.t2.micro|
|ACMCertArn| ACM Certificate for port 443|No default value|
|DockerUser| Docker username|No default value|
|DockerPass| Docker password|No default value|

Once you have configured the parameters. In AWS Cli, please enter this command below and make sure the file paths are correct: 

```bash
aws cloudformation create-stack --stack-name panintelligence /
--template-body file://panintelligence-ecs-deploy.yaml /
--parameters file://parameters.json / 
--capabilities CAPABILITY_NAMED_IAM
```

Once the stack is completed. You will need to obtain the DNS name inside the load balancer.
Please use this command to obtain details:
```bash
aws elb describe-load-balancers --load-balancer-name Panintelligence-ALB
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
