# `echo`

A simple AWS Lambda function.

## Installation

1. Sign up for AWS Lambda
1. Install and configure the `aws` command-line client
1. Create a `lambda-default` role
1. Install the `echo` function

### Sign up for AWS Lambda

Sign up for AWS [**here**](https://aws.amazon.com/).

The Lambda free tier includes 1M free requests per month and 400,000 GB-seconds of compute time per month.

### Install and configure the `aws` command-line client

To install the `aws` command-line client use `pip`:

```
pip install awscli --upgrade --user
```

To configure `aws`, follow these [**quick configuration steps**](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-quick-configuration).

Once configured, you should see `config` and `credentials` files in `~/.aws`.

### Create a `lambda-default` role

The Lambda function will _assume_ a role when executing and will be granted permissions based on the policies attached to this role.

At the very least, we need to create a _basic execution_ role that grants write permissions to CloudWatch Logs. AWS provides one that we can use, `arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole`.

Use `aws iam create-role` and `aws iam attach-role-policy` to create the role and attach the desired policy as follows:

```bash
# Create the role
aws iam create-role \
    --role-name lambda-default \
    --assume-role-policy-document file://.aws/lambda-default-role-policy.json \
    --description "Lambda execution role"

# Attach the policy to the role just created
aws iam attach-role-policy \
    --role-name lambda-default \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

Look up the role to confirm everything looks good, and make a note of the `Arn` returned:

```bash
aws iam get-role \
    --role-name lambda-default
```

### Install the `echo` function

Generate a `.zip` of the source code in `package.zip`:

```bash
# Generate package.zip
zip package echo.py
```

Copy `package.zip` to an S3 bucket that you own:

```bash
# Copy package.zip to your S3 bucket
aws s3 cp package.zip s3://${YOUR_AWS_S3_BUCKET}/lambda/
```

Finally, create the function, remember to specify the `Arn` of your `lambda-default` role:

```bash
# Create your function
aws lambda create-function \
    --publish \
    --runtime python2.7 \
    --role ${YOUR_ARN_LAMBDA_DEFAULT_ROLE} \
    --handler echo.handler \
    --function-name echo \
    --code S3Bucket=${YOUR_AWS_S3_BUCKET},S3Key=lambda/package.zip
```

## Usage

Invoke using `aws lambda invoke`:

```bash
# Invoke the function and save the output to output.txt
aws lambda invoke --function-name echo --payload '["hello", "world"]' output.txt
```

Review the output via:

```bash
cat output.txt
```
