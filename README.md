# Task description

## - Index movie lens content to Elasticsearch
[movie content](https://files.grouplens.org/datasets/movielens/ml-25m-README.html) (movies.csv, ratings.csv, tags.csv)

You could use any way to index data:
- Logstash (csv input, ... )
- Java/Python/C# – Elastic client -> indexing

## - Write console application which search movies

- match phrase (https://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html#more-like-this-query)
- fuzzy
- filter/sort by average rating
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


POST user_ratings/_search
{
  "size": 0,
  "aggs" : {
    "user_rating": {
      "terms": {
        "field": "movieId",
        "order": [{"avg_rating": "desc"}, {"_count": "desc"}]
      },
      "aggs": {
        "avg_rating" : { "avg" : { "field" : "rating" }
          
        }
    }
  }}
}

https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-pipeline-bucket-selector-aggregation.html

POST user_ratings/_search
{
  "size": 0,
  "aggs" : {
    "user_rating": {
      "terms": {
        "field": "movieId",
        "order": [{"avg_rating": "desc"}],
        "size": 10000
      },
      "aggs": {
        "avg_rating" : { "avg" : {
          "field" : "rating"
        }},
        "number_of_counts_bucket_filter": {
          "bucket_selector": {
            "buckets_path": {
              "rated": "_count"
            },
            "script": "params.rated > 500"
          }
        }
      }
    }
  }
}

[171011, 159817, 318, 170705, 158958, 171331, 169022, 171495, 858, 179135]