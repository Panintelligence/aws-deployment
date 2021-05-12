# How to run Panintelligence AWS Cloudformation stack

- Log into AWS management console
- Go into AWS Cloudshell
- Sign into git 
- git clone this project


## Run these commands 

``` BASH
aws cloudformation create-stack --stack-name panintelligence_setup_one --template-body file://phase_2.yml --parameters file://parameters2.json --capabilities CAPABILITY_NAMED_IAM
```
