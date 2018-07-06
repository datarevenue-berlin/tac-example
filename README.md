# Task as Containers example project

## Purpose

This presents how to:
- define tasks and dependencies between them
- execute multiple tasks in parallel and track their outputs
- run everything inside Docker
- run each task in a separate Docker container

## How to run
Clone the repo, `cd` into its root dir and run:
```bash
docker-compose run controller luigi --module tac.task MakePredictions --date 2018-07-05 --scheduler-host scheduler --workers 4
```
Navigate your browser to [http://localhost:8082](http://localhost:8082)
to see a dashboard with defined tasks tree.

## Details
Please read a detailed article at [datarevenue.com](http://datarevenue.com).
