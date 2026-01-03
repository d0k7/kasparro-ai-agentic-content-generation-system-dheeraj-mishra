import pytest
import requests


@pytest.fixture
def base_url():
    return "http://127.0.0.1:5000"


def test_home(base_url):
    response = requests.get(base_url)
    assert response.status_code == 200
    assert "AI Content Generator" in response.text


def test_generate_valid_product_name(base_url):
    response = requests.post(f"{base_url}/api/generate", json={"productName": "Mama Earth Vitamin C Serum"})
    assert response.status_code == 200
    data = response.json()
    assert "questions" in data
    assert "answer" in data


def test_generate_invalid_product_name(base_url):
    response = requests.post(f"{base_url}/api/generate", json={})
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert data["error"] == "productName is required"
