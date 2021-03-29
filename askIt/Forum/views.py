from django.shortcuts import render, HttpResponse
from .crawler import getPosts

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
    if request.method == "POST":
        sQuery = request.POST.get("searchInput")
        print(sQuery)
        #blogs = getPosts(sQuery)
    
    blogs = {'1':{'1':'one','2':'two'},'2':{'1':'one1','2':'two1'},'3':{'1':'one2','2':'two2'}}
    abc={'a':'1','b':'c'}
        
    print(abc)
    return render(request,"postStack.html",abc)

def home1(request):
    return render(request,"postAlumni.html")

def profile(request):
    return render(request,"profile.html")

def profile(request):
    return render(request,"askAlumni.html")



