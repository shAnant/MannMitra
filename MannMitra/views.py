from django.shortcuts import render

def mannMitra(request):
    return render(request,"home.html")

def login(request):
    return render(request,"login.html")

def signin(request):
    return render(request,"signin.html")