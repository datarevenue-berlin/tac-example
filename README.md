# Task as Containers example project

## Purpose

This presents how to:
- define tasks and dependencies between them
- execute multiple tasks in parallel and track their outputs
- run everything inside Docker
- run each task in a separate Docker container

## How to run
- Clone the repo and `cd` into its root.
- Export your AWS credentials into AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
environment variables
- Export name of your S3 bucket name into S3_BUCKET env variable
- Spin up a Minikube cluster
- Build a docker image inside Minikube VM:
```bash
eval $(minikube docker-env)
docker build -t tac-example:v1 . --build-arg AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID --build-arg AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY --build-arg S3_BUCKET=$S3_BUCKET
```
Navigate your browser to [http://localhost:8082](http://localhost:8082)
to see a dashboard with defined tasks tree.

## Details
Please read a detailed article at [datarevenue.com](http://datarevenue.com).
