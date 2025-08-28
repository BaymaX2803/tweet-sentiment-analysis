from fastapi import FastAPI, HTTPException
from .models import Tweet
import ollama
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="LLM Sentiment Analyzer")

HARDCODED_MODELS = [
    "gpt-oss:20b",
    "mistral-nemo:12b",
    "aya:latest",
    "qwen2.5:latest",
    "tinyllama:latest",
    "llama3.2:latest",
    "mistral:latest",
    "deepseek-r1:1.5b"
]

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

@app.get("/models")
def get_models_endpoint():
    logger.info(f"Serving hardcoded model list: {HARDCODED_MODELS}")
    return {"models": HARDCODED_MODELS}

@app.post("/analyze")
def analyze_sentiment(tweet: Tweet):
    if not tweet.text.strip():
        raise HTTPException(status_code=422, detail="Text cannot be empty")
    if not tweet.model:
        raise HTTPException(status_code=422, detail="Model name must be provided")

    logger.info(f"Analyzing sentiment with model: {tweet.model}")

    prompt = f"""
    Analyze the sentiment of the following text and classify it as "positive", "negative", or "neutral".
    Provide your response as a JSON object with two keys: 'label' and 'confidence_scores'.
    The 'label' should be your classification.
    The 'confidence_scores' should be a JSON object with the keys "positive", "negative", and "neutral",
    representing the model's confidence in each classification (values should sum to 1.0).

    Text to analyze: "{tweet.text}"

    JSON Response:
    """

    try:
        response = ollama.generate(
            model=tweet.model,
            prompt=prompt,
            format="json"
        )
        analysis_result = json.loads(response['response'])

        if 'label' not in analysis_result or 'confidence_scores' not in analysis_result:
             raise HTTPException(status_code=500, detail="LLM response was not in the expected format.")

        return analysis_result

    except json.JSONDecodeError:
        logger.error(f"Failed to decode JSON from LLM response: {response.get('response', '')}")
        raise HTTPException(status_code=500, detail="The model did not return valid JSON.")
    except Exception as e:
        logger.error(f"An error occurred while analyzing sentiment: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
