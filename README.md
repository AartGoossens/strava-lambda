# strava-lambda

## Introduction
This is a project that tries to solve one of the big missing parts in the public Strava API: a webhook for updates of following athletes. I tried to solve this by using a lightweight Amazon Lambda function that polls the Strava API for new activities at set intervals and POSTs them to any API.
The Lambda function and related S3 bucket can be deployed using Amazons Free Tier at no cost, but be aware that setting the updated interval in the Lambda function too high may result in additional charges (my [advice](http://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier-alarms.html): set a warning for when you are about to be charged).

## Additional resources:
* [Amazon Lambda website](https://aws.amazon.com/lambda/)
* [Amazon S3 website](https://aws.amazon.com/s3/)
* [Creating Lambda deployment packages](http://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html)
* [AWS SDK for Python](https://aws.amazon.com/sdk-for-python/)
* [Amazon Free Tier](https://aws.amazon.com/free/)

## Work in progress:
* Make code more generic (not specified to Slack)
* Fix authentication issues between Lambda and S3 bucket
* Automate creation of Lambda and bucket using [aws-cli](https://aws.amazon.com/cli/)
* ...
