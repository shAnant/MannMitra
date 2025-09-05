from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os
from scipy.special import softmax

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "roberta-sentiment")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

def predict_emotion(text : str):
    encoded = tokenizer(text,return_tensors="pt")
    
    with torch.no_grad():
        output = model(**encoded)
        
    scores = output.logits[0].detach().numpy()
    probs = softmax(scores)
    
    labels = ["Negative","Neutral","Positive"]
    
    idx = probs.argmax()
    return labels[idx], float(probs[idx])
    