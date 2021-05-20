STACK_NAME=$1

while [ $(aws cloudformation describe-stacks --stack-name ${STACK_NAME} | jq '.Stacks[0].StackStatus') == '"CREATE_IN_PROGRESS"' ]
do
echo "Still Creating"
done
