from django.shortcuts import render, HttpResponse


# def display(request):
#     return render(request,"index.html")
#     # return HttpResponse("login")

def display(request):
    name = "amrut"
    context = {
        "dynamicUserName":name

    }
    return render(request,"index.html",context)

def login(request):
    return render(request,"login.html")

def Register(request):
    return render(request,"register1.html")

def home(request):
    return render(request,"home.html")

