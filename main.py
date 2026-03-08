from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SentimentRequest(BaseModel):
    sentences: List[str]

class SentimentResult(BaseModel):
    sentence: str
    sentiment: str

class SentimentResponse(BaseModel):
    results: List[SentimentResult]

def analyze_sentiment(sentence: str) -> str:
    text = sentence.lower()

    happy_words = [
        # Love & affection
        "love", "adore", "cherish", "affection",
        # Joy & happiness
        "happy", "happiness", "joy", "joyful", "joyous", "delight", "delighted",
        "cheerful", "cheery", "glad", "gleeful", "elated", "ecstatic", "bliss",
        "blissful", "content", "contented", "pleased", "thrilled", "overjoyed",
        # Excitement
        "excited", "exciting", "excitement", "enthusiastic", "enthusiasm",
        "eager", "energetic", "pumped", "stoked",
        # Positivity
        "great", "excellent", "wonderful", "amazing", "fantastic", "awesome",
        "superb", "brilliant", "outstanding", "incredible", "magnificent",
        "splendid", "terrific", "good", "nice", "lovely", "beautiful",
        "perfect", "best", "better", "positive",
        # Gratitude & pride
        "grateful", "thankful", "appreciate", "appreciated", "blessed",
        "proud", "pride", "honor", "triumph",
        # Fun & success
        "fun", "funny", "laugh", "laughing", "smile", "smiling", "grin",
        "win", "winning", "winner", "success", "successful", "achieve",
        "celebrate", "celebration", "congratulations", "congrats",
        # Misc positive
        "like", "enjoy", "enjoying", "enjoyable", "yay", "hooray",
        "fantastic", "refreshing", "peaceful", "relaxed", "comfortable",
        "inspired", "motivated", "confident", "hopeful", "optimistic",
    ]

    sad_words = [
        # Sadness
        "sad", "sadness", "unhappy", "unhappiness", "sorrow", "sorrowful",
        "miserable", "misery", "gloomy", "gloom", "depressed", "depression",
        "grief", "grieve", "grieving", "heartbroken", "heartbreak",
        "devastated", "devastation", "hopeless", "hopelessness",
        # Anger & frustration
        "angry", "anger", "furious", "fury", "rage", "raging", "irritated",
        "irritating", "annoyed", "annoying", "frustrated", "frustrating",
        "frustration", "outraged", "outrage", "bitter", "resentful",
        # Negativity
        "terrible", "awful", "horrible", "dreadful", "atrocious", "appalling",
        "disgusting", "disgust", "revolting", "hideous", "nasty", "dreadful",
        "worst", "bad", "poor", "pathetic", "useless", "worthless",
        # Hate & dislike
        "hate", "hatred", "despise", "detest", "loathe", "dislike",
        # Pain & suffering
        "pain", "painful", "hurt", "hurting", "suffer", "suffering",
        "agony", "agonizing", "torment", "torture", "anguish",
        # Fear & worry
        "fear", "fearful", "afraid", "scared", "terrified", "terror",
        "anxious", "anxiety", "worried", "worry", "panic", "dread",
        "dreading", "nervous", "stress", "stressed", "stressful",
        # Disappointment & regret
        "disappoint", "disappointed", "disappointing", "disappointment",
        "regret", "regretful", "regrets", "sorry", "remorse", "remorseful",
        "fail", "failed", "failure", "miss", "missed", "missing",
        # Loneliness
        "lonely", "loneliness", "alone", "isolated", "isolation",
        "abandoned", "neglected",
        # Tiredness & defeat
        "tired", "exhausted", "exhaustion", "drained", "burnt out",
        "weary", "worn out", "defeated", "helpless", "powerless",
        # Misc negative
        "upset", "cry", "crying", "tears", "sob", "sobbing", "mourn",
        "loss", "lost", "broke", "broken", "damage", "damaged",
        "waste", "wasted", "boring", "bored", "boredom", "ugly",
        "weak", "sick", "ill", "wrong", "mistake", "problem",
        "trouble", "difficult", "hard", "struggle", "struggling",
    ]

    # Check for negation (e.g. "not happy", "don't like", "never good")
    negations = ["not", "no", "never", "don't", "doesn't", "didn't",
                 "won't", "can't", "couldn't", "shouldn't", "isn't", "aren't"]

    words = text.split()
    happy_score = 0
    sad_score = 0

    for i, word in enumerate(words):
        # Check if previous word is a negation
        negated = i > 0 and words[i-1] in negations

        if any(hw in word for hw in happy_words):
            if negated:
                sad_score += 1  # "not happy" = sad
            else:
                happy_score += 1

        if any(sw in word for sw in sad_words):
            if negated:
                happy_score += 1  # "not bad" = happy
            else:
                sad_score += 1

    if happy_score > sad_score:
        return "happy"
    elif sad_score > happy_score:
        return "sad"
    else:
        return "neutral"

@app.api_route("/", methods=["GET", "HEAD", "OPTIONS"])
def root(request: Request):
    return JSONResponse({"status": "ok"})

@app.post("/sentiment", response_model=SentimentResponse)
def sentiment_analysis(request: SentimentRequest):
    results = []
    for sentence in request.sentences:
        sentiment = analyze_sentiment(sentence)
        results.append(SentimentResult(sentence=sentence, sentiment=sentiment))
    return SentimentResponse(results=results)