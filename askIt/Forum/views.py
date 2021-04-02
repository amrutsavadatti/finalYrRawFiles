from django.shortcuts import render, HttpResponse
from .crawler import getPosts
import hashlib

def display(request):
    name = "amrut"
    context = {
        "dynamicUserName":name
    }
    return render(request,"index.html",context)

def login(request):
    return render(request,"login.html")

def takeToHome(request):
    if request.method == "POST":
        name = request.POST.get("name")
        password = request.POST.get("pass")
        print(name,password)
    return render(request,"postAlumni.html")

def alumni(request):
    return render(request,"alumni.html")    

def Register1(request):
    return render(request,"register1.html")

def Register2(request):
    return render(request,"register2.html")

def Register3(request):
    return render(request,"register3.html")

def home(request):
    if request.method == "POST":
        sQuery = request.POST.get("searchInput")
        print(sQuery)
        #blogs = getPosts(sQuery)
    
    blogs = {'1':{'1':'one','2':'two'},'2':{'1':'one1','2':'two1'},'3':{'1':'one2','2':'two2'}}
    abc={'a':'1','b':'c'}
        
    print(abc)
    return render(request,"postAlumni.html",abc)

def encrypt():
    crypt=hashlib.sha256()
    var = "abcdefg"
    crypt.update(bytes(var,'utf-8'))
    print(crypt.hexdigest())


def home1(request):
    return render(request,"postStack.html")

def profile(request):
    return render(request,"profile.html")

def askAlumni(request):
    return render(request,"askAlumni.html")



