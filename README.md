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

## Logging into the dashboard
Follow the link https://<your dashboard public address>:8224 to access your new dashboard.

Upon initial login to the dashboard, you will require a username and password. These are:

Username : admin
Password : <your AWS EC2 Instance ID>
BYOL Only: Obtaining and installing your licence
If you're using the BYOL listing from the marketplace, you will need to install your licence. Please reach out to your account manager for your licence file.

Please log into your instance using ec2-user
Copy your licence to your instance
Execute: sudo su - pi-user
copy your licence to /opt/pi/Dashboard/tomcat/webapps/panLicenceManager/WEB-INF/classes
Your licence file should be called licence.xml
## Deploy Version:Auto Scaling group
In order to

Administrative Considerations
If you followed our recommended setup above, you will need to configure a bastion host for SSH access to the instance as it is in a private subnet.

By default, the ec2-user account can be used to access your deployed AMI image. As part of the stand up, you should have defined a key value pair, please use this when logging in under ssh security

## Logs
Log into the deployed AMI using the ec2-user account.
The dashboard application runs as pi-user. you can log in as that user by running
```
sudo -u pi-user -i
```
Logs are stored under /opt/pi/Dashboard/tomcat/logs/
There are no housekeeping rules set on this folder as default, you may wish to add your own.

## Restarting the Dashboard
To restart the dashboard, please execute:
```
sudo -u pi-user -i
/opt/pi/Dashboard/dashboard.sh all stop
Verify the services have stopped /opt/pi/Dashboard/dashboard.sh all status
/opt/pi/Dashboard/dashboard.sh all start
```
You may verify the the service has restarted /opt/pi/Dashboard/dashboard.sh all status

## Upgrading/backing up the panintelligence dashboard
Please follow these steps when you wish to migrate your panintelligence to a new version of the software which we release regularly or if you wish to upgrade to the developer path (as found in the Marketplace)

We have created 2 scripts for you. They back up key resources which, when applied to a fresh install, will bring all of your changes.

Log into the deployed AMI instance using the ec2-user account.
initiate the backup
```
sudo -u pi-user -i
/opt/pi/Dashboard/s3_backup.sh --s3-bucket=<your s3 bucket name>
```
restore your backup on a new host
Please stop the dashboard prior to running these steps (please see restarting the dashboard)
```
sudo -u pi-user -i
/opt/pi/Dashboard/s3_restore.sh --s3-bucket=<your s3 bucket name> --zip-file=<specify path in s3>
```
If no zip-file option is presented, the restore routine will use the latest backup.
After you've copied the files across to your new host, you can start the dashboard. The database will automatically align to the latest version of the software.

## Infrastructure Diagram
![diagram.png](/images/diagram.png)
