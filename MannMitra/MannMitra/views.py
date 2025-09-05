import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .my_model import predict_emotion

def mannMitra(request):
    return render(request,"home.html")

def login(request):
    return render(request,"login.html")

def signin(request):
    return render(request,"signin.html")

def services(request):
    return render(request,"services.html")

def feeling(request):
    return render(request,"feeling.html")

@csrf_exempt
def analyze_text(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_text = data.get("text","")
        
        if not user_text:
            return JsonResponse({"error":"No text Provided"},status = 400)
        
        emotion, score = predict_emotion(user_text)
        return JsonResponse({"emotion" : emotion, "score":score})
        
        