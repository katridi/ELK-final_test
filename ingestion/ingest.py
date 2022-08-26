import pandas as pd
from tools import extract_year, replace_year, ingest_data, create_elastic_client, set_index_settings

# TOOD adjust path
# TODO put settings in index refresh interval etc
# TODO add IMDBID to user_ratings
ratings_path = "data/ratings.csv"
genome_path =  "data/genome-scores.csv"
genome_tags_path =  "data/genome-tags.csv"
links_path =  "data/links.csv"
movies_path =  "data/movies.csv"
user_tags =  "data/tags.csv"

user_ratings_index = "user_ratings"
movies_index = "movies"

freeze_refresh_interval = {"refresh_interval": "-1"}
unfreeze_refresh_interval = {"refresh_interval": "1s"}

es_client = create_elastic_client()
es_client.ping()

set_index_settings(es=es_client, index_name=user_ratings_index, settings=freeze_refresh_interval)
set_index_settings(es=es_client, index_name=movies_index, settings=freeze_refresh_interval)

print("Read data")

ratings = pd.read_csv(
    ratings_path,
    sep=",",
    usecols=["userId", "movieId", "rating"],
    dtype={"userId": "Int64", "movieId": "Int64", "rating": "float64"},
)

movies = pd.read_csv(movies_path, sep=",")
movies["genres"] = movies["genres"].apply(lambda x: x.split("|"))
movies["year"] = movies["title"].apply(lambda x: extract_year(x)).fillna(0).astype(int)
movies["title"] = movies["title"].apply(lambda x: replace_year(x))


links = pd.read_csv(links_path, sep=",", dtype={"imdbId": "Int64", "tmdbId": "Int64"})
movies_with_links = movies.merge(links, how="left", on="movieId")


ratings_with_names = ratings.merge(movies_with_links, how="left", on="movieId")

print("Ingest user ratings")
ingest_data(es=es_client, data=ratings_with_names, index_name=user_ratings_index)


print("Read data")
genome = pd.read_csv(genome_path, sep=",")
genome_tags = pd.read_csv(genome_tags_path, sep=",")
genome_with_names = genome.merge(genome_tags, how="left", on="tagId")
genome_with_names.drop(axis=0, columns=["tagId"], inplace=True)

grouped_data = pd.DataFrame(columns=("movieId", "tag"))
grouped_by_movie = genome_with_names.groupby("movieId")
for k, v in grouped_by_movie:
    top_10 = v.nlargest(10, "relevance")
    grouped_data = pd.concat([grouped_data, top_10], ignore_index=True)

grouped_tags = grouped_data.groupby("movieId").agg(list)
movies_with_links_and_tags = movies_with_links.merge(grouped_tags, how="left", on="movieId")

movies_with_links_and_tags["tag"] = movies_with_links_and_tags["tag"].apply(lambda d: d if isinstance(d, list) else [])

movies_with_links_and_tags["relevance"] = movies_with_links_and_tags["relevance"].apply(
    lambda d: d if isinstance(d, list) else []
)

print("Ingest movies")
ingest_data(es=es_client, data=movies_with_links_and_tags, index_name=movies_index)

set_index_settings(es=es_client, index_name=user_ratings_index, settings=unfreeze_refresh_interval)
set_index_settings(es=es_client, index_name=movies_index, settings=unfreeze_refresh_interval)

print("Done!")