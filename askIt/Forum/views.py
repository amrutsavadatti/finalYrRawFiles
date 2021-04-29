from django.shortcuts import render, HttpResponse
from .crawler import getPosts
from better_profanity import profanity
from django.views.generic import View
from django.http import JsonResponse
import hashlib
import pyrebase
import random

import csv
from scrap.populate import *
from django.contrib.staticfiles import finders

import requests,json
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    CompoundSearchFilterBackend
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
)

from .documents import *
from .serializers import *

from .models import *


##########################################################
 ##################CONNECT DATABASE#####################
#########################################################

config = {
    "apiKey": "AIzaSyCx1ikG7YyV64HFSJhqe9IEBjKZPvxQXjg",
    "authDomain": "trydata-e39ad.firebaseapp.com",
    "databaseURL": "https://trydata-e39ad-default-rtdb.firebaseio.com",
    "projectId": "trydata-e39ad",
    "storageBucket": "trydata-e39ad.appspot.com",
    "messagingSenderId": "1055915272866",
    "appId": "1:1055915272866:web:35f0eb012e5df50fb245fb"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database = firebase.database()

##########################################################
 ##############CONNECT DATABASE END ###################
#########################################################

class AjaxHandlerView(View):
    def get(self,request):
        alert = "Offensive or inappropriate language used...cant post"
        allGood = "1"
        text = request.GET.get("userPost")
        status = checkProfanity(text)
        if request.is_ajax():
            if(status == True):
                return JsonResponse({"Cuss":alert},status=200)
            elif(text == ""):
                return JsonResponse({"Cuss":"Blank Question cant be posted"},status=200)
            else:
                data={
                    'Question_asked':text,
                    'first_name':"custom_user"
                }
                try:
                    database.child("Questions").child(random.randint(20,10000)).set(data)
                    return JsonResponse({"Cuss":allGood},status=200)
                except:
                    return JsonResponse({"Cuss":"couldnt upload"},status=200)

        return render(request,"askAlumni.html")

# ElasticSearch tutorial 
def generate_random_data():
    url = "https://newsapi.org/v2/everything?q=tesla&from=2021-03-28&sortBy=publishedAt&apiKey=ef39d7a9f9ee4c0ca68745eee26cb99a"
    r = requests.get(url)
    payload = json.loads(r.text)
    count = 1
    for data in payload.get('articles'):
        print(count)
        ElasticDemo.objects.create(
            tittle = data.get('title'),
            content = data.get('description')
        )
        count+=1


def index(request):
    generate_random_data()
    return JsonResponse({'status':200})

class PublisherDocumentView(DocumentViewSet):
    document = NewsDocument
    serializer_class = NewsDocumentSerializer

    filter_backends = [
        FilteringFilterBackend,
        CompoundSearchFilterBackend,
        OrderingFilterBackend,
    ]

    search_fields = ('tittle','content')
    multi_match_search_fields = ('tittle','content')
    filter_fields = {
        'title':'title',
        'content':'content'
    }
    ordering_fields = {
        'id': None,
    }
    ordering = ( 'id'  ,)

# ElasticSearch tutorial End

def display(request):
    name = "amrut"
    context = {
        "dynamicUserName":name
    }
    return render(request,"index.html",context)

def login(request):
    return render(request,"login.html")

def takeToHome(request):

    comb_lst=[]
    if request.method == "POST":
        emailCheck = request.POST.get("email")
        passwordCheck = encrypt(request.POST.get("pass"))
        
        try:
            # user = auth.sign_in_with_email_and_password(email,password)
            getData = UserCreds.objects.all()
            
            for users in getData:
                if users.email == emailCheck and users.password == passwordCheck:
                    request.session['uid'] = users.id

        except:
            message = " Incorrect email or password"
            return render(request,"login.html",{"alertMessage":message})
        
    try:
        Qs = QuestionsAsked.objects.filter(keyLink = request.session['uid'])
        for q in Qs:
            comb_lst.append(q.Question)

        return render(request,"postAlumni.html",{'comb_lst':comb_lst})
    except:
        return HttpResponse("U are logged out")




def alumni(request):
    try:
        request.session['uid']
        
    except:
        return HttpResponse("U are logged out")
    

    try:
        getData = AppUser.objects.all()
        getEData = UserCreds.objects.all()
    except:
        return HttpResponse("Couldnt fetch Data")

    alumniName = []
    alumniEmail = []
    img=[]

    for ppl in getData:
        alumniName.append(ppl.fullName)
    for ppl in getEData:
        alumniEmail.append(ppl.email)
    # request.COOKIES
    for i in range(len(alumniName)):
        img.append(random.randint(1,3))


    # context = {
    #     "name" : alumniName,
    #     "email":alumniEmail,
    #     "img":alumniName

    # }

    info = zip(alumniName,img,alumniEmail)
    return render(request,"alumni.html",{'info':info})
    # return render(request,"alumni.html")    

def Register1(request):
    return render(request,"register1.html")

def Register2(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = encrypt(request.POST.get("pass"))
        fullName = request.POST.get("fullName")
        userName = request.POST.get("userName")
        phoneNumber = request.POST.get("phoneNumber")
        userType = request.POST.get("userType")
        
        putData1 = UserCreds(email=email,password=password)
        putData1.save()
        pk = UserCreds.objects.filter(email=email)

        putData = AppUser(fullName=fullName,userName=userName,phoneNumber=phoneNumber,userType=userType, keyLink=putData1)
        putData.save()

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

def encrypt(var):
    crypt=hashlib.sha256()
    # var = "abcdefg"
    crypt.update(bytes(var,'utf-8'))
    return(crypt.hexdigest())


def home1(request):
    return render(request,"postStack.html")

def profile(request):
    return render(request,"profile.html")

def askAlumni(request):
    return render(request,"askAlumni.html")

def chatBox(request):
    return render(request,"chat.html")

def checkProfanity(comment):
    return profanity.contains_profanity(comment)

def ans(request):
    return render(request,"answers.html")

def LogOut(request):
    try:
        del request.session['uid']
    except KeyError:
        pass
    return render(request,'index.html')




############################################
def populateDb(request):
    try:
        # csv_path = finders.find('C:/Users/Amrut/Desktop/finalYrRawFiles/askIt/scrap/alumniData.csv')
        with open('C:/Users/Amrut/Desktop/finalYrRawFiles/askIt/scrap/alumniData.csv', newline='') as f:
            reader = csv.reader(f)
            data = list(reader)


        for j in range(1,len(data)):
            email = data[j][0]
            passW = encrypt(data[j][1])
            fullName = data[j][2]
            userName = data[j][3]
            phone = data[j][4]
            userT = data[j][5]

            putData1 = UserCreds(email=email,password=passW)
            putData1.save()     


            putData = AppUser(fullName=fullName,userName=userName,phoneNumber=phone,userType=userT, keyLink=putData1)
            putData.save()

        return HttpResponse("status:200")
    except:
        return HttpResponse("Error")

##############################################

def abc(request):
    

    return render(request,"abc.html")
##############################################