#!/bin/bash

# generate next stage yaml file
aws cloudformation package                   \
    --template-file template.yaml            \
    --output-template-file out/output.yaml \
    --s3-bucket antleypk-intuitivewebsolutions-platformengineer-test                     

# the actual deployment step
aws cloudformation deploy                   \
    --template-file out/output.yaml         \
    --stack-name antleypkCodeTest           \
    --capabilities CAPABILITY_IAM             

$SHELL