import pytest

from movies.models import Movie


@pytest.mark.django_db
def test_add_movie(client):

    movies = Movie.objects.all()
    assert len(movies) == 0

    resp = client.post(
        "/api/movies/",
        {"title": "Shutter Island", "year": "2007", "genre": "suspense"},
        content_type="application/json",
    )

    assert resp.status_code == 201
    assert resp.data["title"] == "Shutter Island"

    movies = Movie.objects.all()
    assert len(movies) == 1


@pytest.mark.django_db
def test_add_movie_with_empty_payload(client):

    movies = Movie.objects.all()
    assert len(movies) == 0

    resp = client.post("/api/movies/", {}, content_type="application/json")

    assert resp.status_code == 400

    movies = Movie.objects.all()
    assert len(movies) == 0


@pytest.mark.django_db
def test_add_movie_with_invalid_payload(client):

    movies = Movie.objects.all()
    assert len(movies) == 0

    resp = client.post(
        "/api/movies/",
        {"title": "Shutter Island", "gen": "suspense"},
        content_type="application/json",
    )

    assert resp.status_code == 400

    movies = Movie.objects.all()
    assert len(movies) == 0


@pytest.mark.django_db
def test_get_single_movie(client, add_movie):
    movie = add_movie(title="TestMovie", genre="comedy", year="1998")
    resp = client.get(f"/api/movies/{movie.id}/")
    assert resp.status_code == 200
    assert resp.data["title"] == "TestMovie"


@pytest.mark.django_db
def test_get_all_movies(client, add_movie):
    movie_one = add_movie(title="The Big Lebowski", genre="comedy", year="1998")
    movie_two = add_movie("No Country for Old Men", "thriller", "2007")
    resp = client.get("/api/movies/")
    assert resp.status_code == 200
    assert resp.data[0]["title"] == movie_one.title
    assert resp.data[1]["title"] == movie_two.title


@pytest.mark.django_db
def test_delete_movie(client, add_movie):
    movie_to_delete = add_movie(title="ABC", year="1900", genre="comedy")
    resp = client.delete(f"/api/movies/{movie_to_delete.id}/")
    assert resp.status_code == 204

    resp_two = client.get("/api/movies/")
    assert len(resp_two.data) == 0


@pytest.mark.django_db
def test_update_movie(client, add_movie):
    movie = add_movie(title="The Big Lebowski", genre="comedy", year="1998")

    resp = client.put(
        f"/api/movies/{movie.id}/",
        {"title": "The Big Lebowski", "genre": "comedy", "year": "1997"},
        content_type="application/json",
    )
    assert resp.status_code == 200
    assert resp.data["title"] == "The Big Lebowski"
    assert resp.data["year"] == "1997"

    resp_two = client.get(f"/api/movies/{movie.id}/")
    assert resp_two.status_code == 200
    assert resp_two.data["title"] == "The Big Lebowski"
    assert resp.data["year"] == "1997"


@pytest.mark.django_db
def test_update_movie_incorrect_id(client):
    resp = client.put("/api/movies/99/")
    assert resp.status_code == 404


@pytest.mark.django_db
@pytest.mark.parametrize(
    "add_movie, payload, status_code",
    [
        ["add_movie", {}, 400],
        ["add_movie", {"title": "The Big Lebowski", "genre": "comedy"}, 400],
    ],
    indirect=["add_movie"],
)
def test_update_movie_invalid_json(client, add_movie, payload, status_code):
    movie = add_movie(title="The Big Lebowski", genre="comedy", year="1998")
    resp = client.put(
        f"/api/movies/{movie.id}/",
        payload,
        content_type="application/json",
    )
    assert resp.status_code == status_code
