## Run
docker run -itd --name spark-base-5 pyspark-docker

## Build
docker build -t pyspark-docker .

## Stop
docker stop $(docker ps -a -q)   


## bash
docker exec -it  9028a97a8889 /bin/bash

