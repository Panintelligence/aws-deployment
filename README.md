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

## Cloudformation 

- Download this cloudformation stack:[panintelligence_cloudformation_stack.yaml](/images/panintelligence_cloudformation_stack.yaml)

- Go to AWS console and search for "Cloudformation" and click on "Create stack" on your right:
![cloudform.png](/images/cloudform.png)
- Ensure that "Template is ready" and to specify template you will be uploading the panintelligence cloudformation file. Click next.
![cloudformation_upload.png](/images/cloudformation_upload.png)

- Here you will need to enter these parameters values  and stack name to complete the build:
	- ACMCertArn = The ACM certificate that you have created, you will need to obtain that from "certificate manager to get the arn for that particular certificate.
  - AMIID = The AMI ID that you have obtained when you subscribed to panintelligence product in a particular region of your choice.
  - AvailibilityZoneA = The availibility zone A in your region. 
  - AvailibilityZoneB = The availibility zone B in your region. 
  - MyS3Bucket = The S3 bucket name that you have created in the prerequisites
  ### optional parameters
  - PrivateCidrBlock = The private subnet for your instance to use
  - PublicACidrBlock = One of the public cidr blocks that is in availbility zone A
  - PublicBCidrBlock = One of the public cidr blocks that is in availbility zone B
  - VPCCidrBlock = The cidr block for the VPC
![cloudstackparam.png](/images/cloudstackparam.png)

- Click Next and Click Next again.
- Ensure that you enable "capabilities" and click "create stack".
![endofstack.png](/images/endofstack.png)

- Wait for the stack to complete the build. Refresh until it is built:
![waitingforstack.png](/images/waitingforstack.png)

- Go to your EC2 console and go to loadbalancer and copy the DNS name and paste it into your browser:
![finish.png](/images/finish.png)

- Congratulations, you are now ready to expriment with your data and bring your data to life! 

## Post launch configuration
Finally, we need to create a Route 53 record that aliases to the load balancer.

Navigate to the hosted zone you want to use in Route 53 and create a record set.

Type the subdomain you want to use in the Name field.

Make sure the Type selected is A - IPv4 address and Alias is set to Yes.

In the Alias Target field, start typing the name of the load balancer and select it when it appears.
![alias_target_dropdown.png](/images/alias_target_dropdown.png)

You should now be able to access the dashboard at the domain you configure in the Route 53 record (the DNS entry can sometimes take a little bit to propagate if it doesn't work immediately).

## Infrastructure Diagram
![diagram.png](/imagescloud/cloudformation/diagram.png)
