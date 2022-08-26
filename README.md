# Task description

## - Index movie lens content to Elasticsearch
[movie content](https://files.grouplens.org/datasets/movielens/ml-25m-README.html) (movies.csv, ratings.csv, tags.csv)

You could use any way to index data:
- Logstash (csv input, ... )
- Java/Python/C# – Elastic client -> indexing

## - Write console application which search movies

- match phrase
- fuzzy
- filter/sort by average rating
- finding top-10 tags for the movie
- find movies which userX is put rating of 5).

### NB: Try implement it using several approaches for working with hierarchical data and explain which one is the best fit here

# The implementation

[Tips for speed up ingestion](https://www.elastic.co/guide/en/elasticsearch/reference/current/tune-for-indexing-speed.html)

## Build image for ingestion

``` bash
sudo docker build -t movies_ingestion -f ingestion/Dockerfile .
```

## Map data volume from here [movie content](https://files.grouplens.org/datasets/movielens/ml-25m-README.html) (movies.csv, ratings.csv, tags.csv) and run ingestion

``` bash
docker run --network=host -it  -v $("pwd")/data:/app/data movies_ingestion
```

# Build docker image

``` bash
sudo docker build -t movies_searcher -f docker/Dockerfile .
```

# Run image

``` bash
docker run --network=host -it movies_searcher
```

# Usage within container

## For simplicity `movie` alias is used to run the app in container

