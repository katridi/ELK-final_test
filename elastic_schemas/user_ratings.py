from elasticsearch_dsl import Document, Integer, Keyword, Text, Float


class UserRatings(Document):
    user_id = Integer()
    movieId = Integer()
    rating = Float()
    title = Text()
    genres = Keyword()
    year = Integer()

    class Index:
        name = 'user_ratings'
        settings = {
          "refresh_interval" : "1",
          "number_of_shards" : "1",
        }

    def title_and_year(self) -> str:
        return f'| {self.title} | {self.year} |'
