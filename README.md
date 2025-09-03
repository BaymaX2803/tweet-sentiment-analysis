# LLM Sentiment Analyzer

A full-stack application for sentiment analysis using Large Language Models (LLMs) via [Ollama](https://ollama.com/). The project features a FastAPI backend and a Streamlit frontend, both containerized with Docker and orchestrated via Docker Compose. The backend communicates with Ollama to analyze sentiment, while the frontend provides an interactive UI for users.

---

## Features

- **FastAPI Backend**: Exposes REST endpoints for health checks, model listing, and sentiment analysis.
- **Streamlit Frontend**: User-friendly web interface for submitting text and visualizing sentiment results.
- **Ollama Integration**: Supports multiple LLMs (e.g., Mistral, Llama3, Aya) for flexible sentiment analysis.
- **Dockerized**: Both frontend and backend are containerized for easy deployment and development.
- **CI/CD**: Automated testing and Docker image publishing via GitHub Actions.

---

## Project Structure

```
.
├── backend/
│   ├── main.py          # FastAPI app with sentiment endpoints
│   ├── models.py        # Pydantic models for request validation
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── app.py           # Streamlit UI
│   ├── requirements.txt
│   └── Dockerfile
├── tests/
│   └── test_backend.py  # Pytest-based backend tests
├── docker-compose.yml   # Multi-service orchestration
└── .github/workflows/ci-cd.yml # CI/CD pipeline
```

---

## Technical Details

### Backend

- **Framework**: FastAPI
- **Endpoints**:
  - `GET /health`: Health check
  - `GET /models`: List available LLM models
  - `POST /analyze`: Analyze sentiment of input text using a selected model
- **Ollama Integration**: Uses the `ollama` Python package to send prompts and receive structured JSON responses from LLMs.
- **Validation**: Uses Pydantic models for input validation and error handling.

### Frontend

- **Framework**: Streamlit
- **Features**:
  - Model selection from backend-provided list
  - Text input for sentiment analysis
  - Visualization of sentiment label and confidence scores
- **Backend Communication**: Uses REST API calls to the backend service.

### Docker & Compose

- **Backend**: Runs on port 8000, source code mounted for live reload in development.
- **Frontend**: Runs on port 8501, connects to backend via environment variable.
- **Ollama**: Expected to be running separately (see [Ollama documentation](https://ollama.com/docs)).
- **Networking**: Both services share a Docker network for internal communication.

### CI/CD

- **GitHub Actions**: Workflow for testing (with Ollama service), building, and pushing Docker images.
- **Tests**: Pytest-based tests for backend endpoints, including model integration.

---

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/)
- [Ollama](https://ollama.com/) running locally or accessible from Docker containers

### Development

1. **Clone the repository**
2. **Start Ollama** and pull the required models (e.g., `ollama pull mistral:latest`)
3. **Run the stack**:
   ```sh
   docker-compose up --build
   ```
4. **Access the frontend**: [http://localhost:8501](http://localhost:8501)
5. **API docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

### Running Tests

```sh
pip install -r backend/requirements.txt
pip install pytest
pytest tests/
```

---

## Configuration

- **Model List**: Hardcoded in main.py as `HARDCODED_MODELS`.
- **Backend URL**: Set via `BACKEND_URL` environment variable for the frontend.
- **Ollama Host**: Set via `OLLAMA_HOST` environment variable for the backend.

---
