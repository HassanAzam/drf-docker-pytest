import pytest

from movies.models import Movie


@pytest.fixture(scope="function")
def add_movie():
    def _add_movie(title, genre, year):
        movie = Movie.objects.create(title=title, year=year, genre=genre)
        return movie

    return _add_movie
