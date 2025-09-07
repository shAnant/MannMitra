import json
from django.shortcuts import redirect,render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .my_model import predict_emotion
from .models import UserProfile
from django.contrib import messages

def mannMitra(request):
    is_user_authorized = True if "email" in request.session else False
    return render(request,"home.html",{"is_user_authorized":is_user_authorized})

def login(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        print(f"email: {email}\npassword: {password}")
        try:
            
            user = UserProfile.objects.get(email=email,password=password)
            request.session["email"] = user.email
            request.session["password"] = user.password
            request.session["username"] = user.username
            return redirect("services")
        except UserProfile.DoesNotExist:
            messages.error(request,"Invalid username or password")
    
    return render(request,"login.html")

def logout(request):
    if "email" in request.session:
        del request.session["email"]
        del request.session["password"]
        del request.session["username"]
    return redirect('/')


def services(request):
    return render(request,"services.html") if 'email' in request.session else redirect('login')

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
        
def signin(request):
    if request.method == 'POST':        
        fullname = request.POST.get("fullname")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")
        
        if password != confirm:
            return render(request,"signin.html",{"error":"Password doesn't match"})
        
        if UserProfile.objects.filter(username=username).exists():
            return render(request,"signin.html",{"error":"User name already taken"})
        
        if UserProfile.objects.filter(email=email).exists():
            return render(request,"signin.html",{"error":"Email already exists"})
        
        user = UserProfile(fullname=fullname, username=username,email=email,password=password)
        user.save()
        
        return redirect("login")
    return render(request,"signin.html")