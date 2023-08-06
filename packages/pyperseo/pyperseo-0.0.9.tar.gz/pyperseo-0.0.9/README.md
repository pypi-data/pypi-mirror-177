# SEMANTIC FUNCTIONALITIES


**Pull the image in your local from [Dockerhub](https://hub.docker.com/repository/docker/pabloalarconm/perseo):**

`docker pull pabloalarconm/perseo:latest`

<hr>

##  Unique identifier generator:

Milisecond timestamp for CSV spreadsheets

**Run the docker by pointing your CSV files as a volume to `/app/data` It will take all CSVs from this directory and transform all of them:**

`docker run --rm -v /path/of/your/volumes:/app/data pabloalarconm/perseo uniqid`

**If you dont point to any volume:** `docker run --rm pabloalarconm/perseo uniqid`. **Docker will run the default mock CSV files included in** `/app/data` **named** `trial.csv`


## NT to TTL transformation

RDF data transformation from N-Triples representation to Turtle

**Run the docker by pointing your N-Triples files as a volume to `/app/data` It will take all CSVs from this directory and transform all of them:**

`docker run --rm -v /path/of/your/volumes:/app/data pabloalarconm/perseo 2ttl`


