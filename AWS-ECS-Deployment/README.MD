# ECS deployment


```
aws cloudformation create-stack --stack-name panintelligence /
--template-body file://panintelligence-ecs-deploy.yaml /
--parameters file://parameters.json / 
--capabilities CAPABILITY_NAMED_IAM
```
