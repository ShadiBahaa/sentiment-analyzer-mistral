from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sentiment Analyzer API", version="1.0.0")

# Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Sentiment Analyzer API is running!"}

@app.post("/analyze/")
def analyze_sentiment(text: str = Form(...)):
    """
    Analyze the sentiment of the provided text using Mistral model via Ollama.
    
    Args:
        text (str): The text to analyze
        
    Returns:
        dict: Contains the predicted sentiment
    """
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    try:
        # Create a more specific prompt for better sentiment classification
        prompt = f"""Analyze the sentiment of the following text and respond with exactly one word: Positive, Negative, or Neutral.

Text: "{text}"

Sentiment:"""

        # Make request to Ollama
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral", 
                "prompt": prompt, 
                "stream": False,
                "options": {
                    "temperature": 0.1,  # Lower temperature for more consistent results
                    "top_p": 0.9,
                    "num_predict": 10  # Limit response length for single word answers
                }
            },
            timeout=30  # Add timeout to prevent hanging
        )
        
        if response.status_code != 200:
            logger.error(f"Ollama request failed with status {response.status_code}")
            raise HTTPException(status_code=500, detail="Failed to connect to Ollama service")
        
        result = response.json()
        sentiment_raw = result["response"].strip()
        
        # Clean and validate the response
        sentiment_clean = sentiment_raw.split('\n')[0].strip().title()
        
        # Ensure the response is one of the expected values
        valid_sentiments = ["Positive", "Negative", "Neutral"]
        if sentiment_clean not in valid_sentiments:
            # Try to extract sentiment from response if it's not exact
            sentiment_lower = sentiment_clean.lower()
            if "positive" in sentiment_lower:
                sentiment_clean = "Positive"
            elif "negative" in sentiment_lower:
                sentiment_clean = "Negative"
            else:
                sentiment_clean = "Neutral"
        
        logger.info(f"Analyzed text: '{text[:50]}...' -> Sentiment: {sentiment_clean}")
        
        return {
            "sentiment": sentiment_clean,
            "text": text,
            "raw_response": sentiment_raw
        }
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Request to Ollama failed: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Could not connect to Ollama service. Make sure Ollama is running and Mistral model is available."
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@app.get("/health/")
def health_check():
    """Check if the API and Ollama service are healthy."""
    try:
        # Test connection to Ollama
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json()
            mistral_available = any(model["name"].startswith("mistral") for model in models["models"])
            return {
                "api_status": "healthy",
                "ollama_status": "connected",
                "mistral_available": mistral_available
            }
        else:
            return {
                "api_status": "healthy",
                "ollama_status": "error",
                "mistral_available": False
            }
    except Exception as e:
        return {
            "api_status": "healthy",
            "ollama_status": "disconnected",
            "mistral_available": False,
            "error": str(e)
        }