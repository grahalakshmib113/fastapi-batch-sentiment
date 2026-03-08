from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Step A: Define what the incoming request looks like
class SentimentRequest(BaseModel):
    sentences: List[str]

# Step B: Define what one result looks like
class SentimentResult(BaseModel):
    sentence: str
    sentiment: str

# Step C: Define what the full response looks like
class SentimentResponse(BaseModel):
    results: List[SentimentResult]

# Step D: The actual mood-detection logic
def analyze_sentiment(sentence: str) -> str:
    text = sentence.lower()  # Make everything lowercase so "Happy" == "happy"

    happy_words = [
        "love", "happy", "great", "excellent", "wonderful", "amazing",
        "fantastic", "good", "best", "joy", "excited", "glad", "awesome",
        "brilliant", "superb", "delightful", "proud", "thankful", "nice",
        "beautiful", "perfect", "fun", "yay", "laugh", "smile", "win",
        "celebrate", "like", "enjoy", "pleased", "thrilled"
    ]

    sad_words = [
        "sad", "terrible", "awful", "horrible", "hate", "worst", "bad",
        "disappoint", "upset", "cry", "miss", "lonely", "depressed",
        "unfortunate", "regret", "sorry", "fail", "loss", "hurt", "pain",
        "angry", "frustrated", "annoyed", "boring", "waste", "tired",
        "exhausted", "broke", "broken", "terrible", "dread", "fear"
    ]

    happy_score = sum(1 for word in happy_words if word in text)
    sad_score = sum(1 for word in sad_words if word in text)

    if happy_score > sad_score:
        return "happy"
    elif sad_score > happy_score:
        return "sad"
    else:
        return "neutral"

# Step E: The actual API endpoint
@app.post("/sentiment", response_model=SentimentResponse)
def sentiment_analysis(request: SentimentRequest):
    results = []
    for sentence in request.sentences:
        sentiment = analyze_sentiment(sentence)
        results.append(SentimentResult(sentence=sentence, sentiment=sentiment))
    return SentimentResponse(results=results)