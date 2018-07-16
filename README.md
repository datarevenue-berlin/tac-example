# Task as Containers example project

## Details
Please read the detailed article at [Data Revenue's Blog](https://www.datarevenue.com/blog/).

## How to run
- Clone the repo and `cd` into its root.
- Install requirements and the project itself.
- Export your [AWS credentials](https://console.aws.amazon.com/iam/home#/security_credential) 
into AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables.
- Export name of your S3 bucket name into S3_BUCKET env variable.
- Spin up a Minikube cluster.
- Build a docker image inside Minikube VM:
```bash
eval $(minikube docker-env)
docker build -t tac-example:v1 . --build-arg AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID --build-arg AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY --build-arg S3_BUCKET=$S3_BUCKET
```
- Run the pipeline:
```bash
luigi --module tac.task MakePredictions --date 2018-01-01
```
