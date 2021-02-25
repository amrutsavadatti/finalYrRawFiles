from django.shortcuts import render, HttpResponse


def display(request):
    return render(request,"index.html")
    # return HttpResponse("login")

def login(request):
    name = "amrut"
    context = {
        "dynamicUserName":name

    }
    return render(request,"login.html",context)

def Register(request):
    return render(request,"register.html")

