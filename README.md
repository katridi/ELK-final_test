# Task description

## - Index movie lens content to Elasticsearch
[movie content](https://files.grouplens.org/datasets/movielens/ml-25m-README.html) (movies.csv, ratings.csv, tags.csv)

You could use any way to index data:
- Logstash (csv input, ... )
- Java/Python/C# – Elastic client -> indexing

## - Write console application which search movies

- match phrase (https://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html#more-like-this-query)
- fuzzy
- filter/sort by average rating <b>(DONE)</b>
- finding top-10 tags for the movie <b>(DONE)</b>
- find movies which userX is put rating of 5). <b>(DONE)</b>

### NB: Try implement it using several approaches for working with hierarchical data and explain which one is the best fit here

# The implementation

[Tips for speed up ingestion](https://www.elastic.co/guide/en/elasticsearch/reference/current/tune-for-indexing-speed.html)

DELETE user_ratings

PUT user_ratings

PUT user_ratings/_settings
{
  "index" : {
    "refresh_interval" : "-1"
  }
}

GET user_ratings/_settings



DELETE movies

PUT movies

PUT movies/_settings
{
  "index" : {
    "refresh_interval" : "-1"
  }
}

GET movies/_settings

# TODO add IMDB_id url to output


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
