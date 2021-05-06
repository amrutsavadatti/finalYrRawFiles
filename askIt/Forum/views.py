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

from .checkDoc import*
from django.core.files.storage import FileSystemStorage
import os



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
        try:
            request.session['uid']
            
        except:
            return HttpResponse("U are logged out")
        

        try:
            getData = UserInfo.objects.all()
            getEData = UserCred.objects.all()
        except:
            return HttpResponse("Couldnt fetch Data")

        alumniName = []
        alumniEmail = []
        img=[]

        for ppl in getData:
            alumniName.append(ppl.fullName)
        for ppl in getEData:
            alumniEmail.append(ppl.email)

        for i in range(len(alumniName)):
            img.append(random.randint(1,3))

        info = zip(alumniName,img,alumniEmail)
        
        return render(request,"askAlumni.html",{'info':info})

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

# class PublisherDocumentView(DocumentViewSet):
#     document = AnsDocument
#     serializer_class = AnsDocumentSerializer

#     filter_backends = [
#         FilteringFilterBackend,
#         CompoundSearchFilterBackend,
#         OrderingFilterBackend,
#     ]

#     search_fields = ('answer','content')
#     multi_match_search_fields = ('tittle','content')
#     filter_fields = {
#         'title':'title',
#         'content':'content'
#     }
#     ordering_fields = {
#         'id': None,
#     }
#     ordering = ( 'id'  ,)


class PublisherDocumentView(DocumentViewSet):
    document = AnsDocument
    serializer_class = AnsDocumentSerializer

    filter_backends = [
        FilteringFilterBackend,
        CompoundSearchFilterBackend,
        OrderingFilterBackend,
    ]

    search_fields = ('answer','ansTo')
    multi_match_search_fields = ('answer','ansTo')
    filter_fields = {
        'answer':'answer',
        'ansTo':'ansTo'
        
    }
    ordering_fields = {
        'id': None,
    }
    ordering = ( 'id')


   

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
        passwordCheck = request.POST.get("pass")
        
        try:
            # user = auth.sign_in_with_email_and_password(email,password)
            getData = UserCred.objects.all()
            
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
        return render(request,"postAlumni.html",{'comb_lst':comb_lst})




def alumni(request):
    try:
        request.session['uid']
        
    except:
        return HttpResponse("U are logged out")
    

    try:
        getData = AppUser.objects.all()
        getEData = UserCred.objects.all()
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


    info = zip(alumniName,img,alumniEmail)
    return render(request,"alumni.html",{'info':info})
  

def Register1(request):
    return render(request,"register1.html")

def Register2(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = encrypt(request.POST.get("pass"))
        fullName = request.POST.get("fullName")
        userName = request.POST.get("userName")
        phoneNumber = request.POST.get("phoneNumber")
        # userType = request.POST.get("userType")
        userType = "alumni"
        
        putData1 = UserCred(email=email,password=password)
        putData1.save()
        pk = UserCred.objects.filter(email=email)

        putData = AppUser(fullName=fullName,userName=userName,phoneNumber=phoneNumber,userType=userType, keyLink=putData1)
        putData.save()

    return render(request,"register2.html")

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
    crypt.update(bytes(var,'utf-8'))
    return(crypt.hexdigest())


def home1(request):
    try:
        request.session['uid']
    
    except:
        return HttpResponse("U are logged out")

    return render(request,"postStack.html")

def profile(request):
    try:
        request.session['uid']
    
    except:
        return HttpResponse("U are logged out")
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

def runCheck(request):
    uploaded_file = 0
    if request.method == "POST":

        base_dir = "C:/Users/Amrut/Desktop/askIt/finalYrRawFiles/askIt/askIt/media"
        for f in os.listdir(base_dir):
            os.remove(os.path.join(base_dir, f))

        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name,uploaded_file)
    else:
        return render(request,"register3.html")
    if(uploaded_file != 0):
        base_dir = "C:/Users/Amrut/Desktop/askIt/finalYrRawFiles/askIt/askIt/media"
        fileList = os.listdir(base_dir)
        print(fileList)
        image = os.path.join(base_dir,fileList[0])
        print(image)

        ans = execute(image)

        if ans == "1":
            return render(request,"postAlumni.html",{"ans":"You Are All Set To Go !!"})
        elif ans == "-1":
            return render(request,"register3.html",{"err":"Make sure image is readable"})
        else:
            return render(request,"register3.html",{"err":"Uploaded document does not appear to be SFIT Marksheet"})


    # ans = execute()
    # print(ans)
    # return HttpResponse("DOne")


############################################

# # TO POPULATE QnA

# def populateDb(request):
#     # try:
#     pk = UserCred.objects.filter(email="tarun@gmail.com")
#     print(pk[0])
#     # csv_path = finders.find('C:/Users/Amrut/Desktop/finalYrRawFiles/askIt/scrap/alumniData.csv')
#     with open('C:/Users/Amrut/Desktop/askIt/finalYrRawFiles/askIt/scrap/QnA.csv', newline='') as f:
#         reader = csv.reader(f)
#         data = list(reader)


#     for j in range(2,len(data)):
#         print("Question")
#         qstn = data[j][0]
#         print(qstn)
#         putData1 = Questions(question=qstn,userWhoAsked=pk[0] )
#         putData1.save() 
#         for i in range(1,3):
#             print(data[j][i])
#             putData = Answers(answer=data[j][i],ansTo=putData1)
#             putData.save()

#     return HttpResponse("status:200")
#     # except:
#     #     return HttpResponse("Error")


#TO POPULATE USERS
def populateDb(request):
    # try:
        # csv_path = finders.find('C:/Users/Amrut/Desktop/finalYrRawFiles/askIt/scrap/alumniData.csv')
    with open('C:/Users/Amrut/Desktop/askIt/finalYrRawFiles/askIt/scrap/alumniData.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)


    for j in range(1,len(data)):
        email = data[j][0]
        passW = encrypt(data[j][1])
        fullName = data[j][2]
        userName = data[j][3]
        phone = data[j][4]
        userT = data[j][5]

        putData1 = UserCred(email=email,password=passW)
        putData1.save()     


        putData = UserInfo(fullName=fullName,userName=userName,phoneNumber=phone,userType=userT, keyLink=putData1)
        putData.save()

    return HttpResponse("status:200")
    # except:
    #     return HttpResponse("Error")

##############################################

def abc(request):

    return render(request,"abc.html")
##############################################