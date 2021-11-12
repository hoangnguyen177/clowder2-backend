from fastapi.testclient import TestClient

from app.main import app
from app.main import API_V2_STR


client = TestClient(app)

dataset = {
    "name": "first dataset",
    "description": "a dataset is a container of files and metadata",
    "views": 0,
    "downloads": 0,
}

user = {"name": "test@test.org", "password": "not_a_password"}


def test_create():
    response = client.post(f"{API_V2_STR}/users/", json=user)
    assert response.status_code == 200
    response = client.post(f"{API_V2_STR}/login", json=user)
    assert response.status_code == 200
    token = response.json().get("token")
    assert token is not None
    headers = {"Authorization": "Bearer " + token}
    response = client.post(f"{API_V2_STR}/datasets/", json=dataset, headers=headers)
    assert response.json().get("id") is not None
    assert response.status_code == 200


def test_get_one():
    response = client.post(f"{API_V2_STR}/login", json=user)
    assert response.status_code == 200
    token = response.json().get("token")
    assert token is not None
    headers = {"Authorization": "Bearer " + token}
    response = client.post(f"{API_V2_STR}/datasets/", json=dataset, headers=headers)
    assert response.json().get("id") is not None
    assert response.status_code == 200
    dataset_id = response.json().get("id")
    response = client.get(f"{API_V2_STR}/datasets/{dataset_id}")
    assert response.status_code == 200
    assert response.json().get("id") is not None


def test_list():
    response = client.post(f"{API_V2_STR}/login", json=user)
    assert response.status_code == 200
    token = response.json().get("token")
    assert token is not None
    headers = {"Authorization": "Bearer " + token}
    response = client.post(f"{API_V2_STR}/datasets/", json=dataset, headers=headers)
    assert response.json().get("id") is not None
    assert response.status_code == 200
    response = client.get(f"{API_V2_STR}/datasets/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0
