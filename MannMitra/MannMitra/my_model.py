import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SENTIMENT_MODEL_PATH = os.path.join(BASE_DIR, "py_models", "roberta-sentiment")

tokenizer = None
model = None
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # real device

def load_model():
    global tokenizer, model
    if tokenizer is None or model is None:
        tokenizer = AutoTokenizer.from_pretrained(SENTIMENT_MODEL_PATH)
        model = AutoModelForSequenceClassification.from_pretrained(SENTIMENT_MODEL_PATH)
        model.to(device)  # move model to real device
        model.eval()
    return tokenizer, model

def predict_emotion(text):
    tokenizer, model = load_model()
    encoded = tokenizer(text, return_tensors="pt").to(device)  # move input to same device

    with torch.no_grad():
        output = model(**encoded)
        scores = torch.nn.functional.softmax(output.logits, dim=1)[0]
        predicted_class = int(torch.argmax(scores).cpu())  # move to CPU before converting
        confidence = float(scores[predicted_class].cpu())

    id2label = model.config.id2label
    label = id2label.get(predicted_class, str(predicted_class))
    
    if label == 'LABEL_1':label = "Neutral"
    if label == 'LABEL_0':label = "Negative"
    if label == 'LABEL_2':label = "Positive"

    return label, confidence
