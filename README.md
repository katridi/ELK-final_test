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
