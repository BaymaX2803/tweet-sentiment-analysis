# tests/test_backend.py
import sys
import os

# Add the parent directory to the Python path so we can import from backend
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

# Use a valid model from HARDCODED_MODELS
TEST_MODEL = "mistral:latest"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_positive_sentiment():
    response = client.post("/analyze", json={
        "text": "I love this product!",
        "model": TEST_MODEL
    })
    assert response.status_code == 200
    data = response.json()
    assert data["label"] in ["positive", "neutral", "negative"]
    assert "confidence_scores" in data
    assert set(data["confidence_scores"].keys()) == {"positive", "negative", "neutral"}


def test_negative_sentiment():
    response = client.post("/analyze", json={
        "text": "C'est terrible, je déteste ça.",
        "model": TEST_MODEL
    })
    assert response.status_code == 200
    data = response.json()
    assert data["label"] in ["positive", "neutral", "negative"]
    assert "confidence_scores" in data


def test_empty_tweet():
    response = client.post("/analyze", json={
        "text": "",
        "model": TEST_MODEL
    })
    assert response.status_code == 422
    assert response.json()["detail"] == "Text cannot be empty"


def test_missing_model():
    response = client.post("/analyze", json={
        "text": "This should fail because model is missing"
    })
    assert response.status_code == 422
    data = response.json()
    assert isinstance(data["detail"], list)
    assert data["detail"][0]["loc"] == ["body", "model"]
    assert data["detail"][0]["msg"] == "Field required"