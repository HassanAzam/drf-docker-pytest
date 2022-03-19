from django.urls import reverse
import json

def test_hello_world():
	assert "helloworld" == "helloworld"
	assert "foo" != "bar"

def test_ping(client):
	url = reverse("ping")
	response = client.get(url)
	content = json.loads(response.content)
	assert response.status_code == 200
	assert content["ping"] == "pong"

