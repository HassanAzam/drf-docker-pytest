
import pytest

from movies.models import Movie

@pytest.mark.django_db
def test_movie_model():
    movie = Movie(title="The Batman", genre="thriller", year="2022")
    movie.save()
    assert movie.title == "The Batman"
    assert movie.genre == "thriller"
    assert movie.year == "2022"
    assert movie.created_date
    assert movie.updated_date
    assert str(movie) == movie.title
