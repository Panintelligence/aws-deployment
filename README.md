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

