from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from .crawler import *
from better_profanity import profanity
from textblob import TextBlob
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
from rest_framework.response import Response

from .documents import *
from .serializers import *
from .models import *

from .checkDoc import*
from django.core.files.storage import FileSystemStorage
import os


from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from .w2v import *
from django.views.decorators.csrf import csrf_exempt




def getSkills(request):
    ans=test("how to make lists using c++")
    print(ans)
    return render(request,"askAlumni.html")


def tattiFun(request):
    usr = request.user#gives username
    print(request.user.first_name)
    return render(request,'tattiIdea.html')

@csrf_exempt
def AskAlumni(request):
    if request.method == "POST":
        alert = "Offensive or inappropriate language used...cant post"
        allGood = "1"
        text = request.POST["userPost"]
        alumni = request.POST['alumniID']
        status = checkProfanity(text)
        if(status == True):
            return JsonResponse({"Cuss":alert},status=200)
        elif(text == ""):
            return JsonResponse({"Cuss":"Blank Question cant be posted"},status=200)
        else:
            try:
                usr = User.objects.filter(username = request.user).first()
                qtn = Questions(question = text,userWhoAsked = usr)
                qtn.save()
                alumniUsrObj = User.objects.filter(id=alumni).first()
                nfy = Notifications(question = text,whoAsked = request.user, user = alumniUsrObj, qID = qtn.id)
                nfy.save()
                return JsonResponse({"Cuss":allGood},status=200)
            except:
                return JsonResponse({"Cuss":"couldnt upload"},status=200)
    try:
        #gets related skills here
        qtn = request.session["cachedQtn"]
        # print(qtn)
        ans=test(qtn)
        # print(ans)

        skillSet = [item.id for skill in ans for item in Skills.objects.filter(skill = skill)]
        print(skillSet)
        usersSet = set([user.user for skill in skillSet for user in  userSkills.objects.filter(skill = skill)])
        print(usersSet)

        userToPrint = [user for obj in usersSet for user in  UserInfo.objects.filter(user = obj, is_verified = True ,userType = "alumni",markSheet_verified = True)]
        
        alumniName = [f"{ppl.user.first_name} {ppl.user.last_name}" for ppl in userToPrint]
        print(alumniName)
        alumniEmail = [ppl.user.email for ppl in userToPrint]
        img=[random.randint(1,3) for i in range(len(alumniName))]
        alumniUsr = [a.user.id for a in userToPrint]
        print(alumniUsr)


        info = zip(alumniName,img,alumniEmail,alumniUsr)

        # info = [(f"{ppl.user.first_name} {ppl.user.last_name}", ppl.user.email, random.randint(1, 3)) for ppl, in getUserInfo)]
        
        
        return render(request,"askAlumni.html",{'info':info})
    except:
        return render(request,"askAlumni.html")


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
                try:
                    usr = User.objects.filter(username = request.user).first()
                    qtn = Questions(question = text,userWhoAsked = usr)
                    qtn.save()
                    return JsonResponse({"Cuss":allGood},status=200)
                except:
                    return JsonResponse({"Cuss":"couldnt upload"},status=200)

        try:
            #gets related skills here
            qtn = request.session["cachedQtn"]
            # print(qtn)
            ans=test(qtn)
            # print(ans)

            skillSet = [item.id for skill in ans for item in Skills.objects.filter(skill = skill)]
            print(skillSet)
            usersSet = set([user.user for skill in skillSet for user in  userSkills.objects.filter(skill = skill)])
            print(usersSet)

            userToPrint = [user for obj in usersSet for user in  UserInfo.objects.filter(user = obj, is_verified = True ,userType = "alumni",markSheet_verified = True)]
            
            alumniName = [f"{ppl.user.first_name} {ppl.user.last_name}" for ppl in userToPrint]
            print(alumniName)
            alumniEmail = [ppl.user.email for ppl in userToPrint]
            img=[random.randint(1,3) for i in range(len(alumniName))]

            info = zip(alumniName,img,alumniEmail)

            # info = [(f"{ppl.user.first_name} {ppl.user.last_name}", ppl.user.email, random.randint(1, 3)) for ppl, in getUserInfo)]
            
            
            return render(request,"askAlumni.html",{'info':info})
        except:
            return render(request,"askAlumni.html")



class PublisherDocumentView(DocumentViewSet):
    
    document = AnsDocument
    serializer_class = AnsDocumentSerializer

    filter_backends = [
        FilteringFilterBackend,
        CompoundSearchFilterBackend,
        OrderingFilterBackend,
    ]

    search_fields = ('answer','ansTo','ansTo__question')
    multi_match_search_fields = ('answer','ansTo','ansTo__question')
    filter_fields = {
        'answer':'answer',
        'ansTo':'ansTo'   
    }
    ordering_fields = {
        'id': None,
    }
    ordering = ( 'id')
    
        

def login_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = encrypt(request.POST.get("pass"))
        print(username,password)
        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('/accounts/login')
               
        profile_obj = UserInfo.objects.filter(user = user_obj ).first()

        if not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified check your mail.')
            return redirect('/accounts/login')

        user = authenticate(username = username , password = password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('/accounts/login')
        
        login(request , user)
        return redirect('/getIn')

    return render(request , 'login.html')

@login_required
def getIn(request):
    #put recent questions here
    return render(request,"postAlumni.html")


@login_required
def Account(request):
    if request.method == "POST" and request.POST.get("searchInput")!=None:
        base = "http://127.0.0.1:8000/search/?search="
        # print(requests.get("http://127.0.0.1:8000/search/?search=django").json())
        sQuery = request.POST.get("searchInput")
        op = requests.get(base+sQuery).json()
        print(op)
        print(op[0]['ansTo']['id'])
        qList = []
        idList=[]
        id = -1
        for i in range(len(op)):
            if op[i]['ansTo']['id']!=id:
                qList.append(op[i]['ansTo']['question'])
                id=op[i]['ansTo']['id']
                idList.append(id)
        print(qList)
        info = zip(idList,qList)                
        return render(request,"postAlumni.html",{'info':info})
    return render(request,"postAlumni.html")

@login_required
def takeToHome(request):
    if request.method == "POST" and request.POST.get("searchInput")!=None:
        base = "http://127.0.0.1:8000/search/?search="

        # print(requests.get("http://127.0.0.1:8000/search/?search=django").json())

        sQuery = request.session["cachedQtn"] = request.POST.get("searchInput")
        print("#" + sQuery)
        op = requests.get(base+sQuery).json()
        request.session['previousSearch'] = op
        # print(op)
        # print(op[0]['ansTo']['id'])
        qList = []
        idList=[]
        ansList=[]
        id = -1
        for i in range(len(op)):
            if op[i]['ansTo']['id']!=id:
                qList.append(op[i]['ansTo']['question'])
                id=op[i]['ansTo']['id']
                idList.append(id)
                ansList.append(op[i]['answer'][0:100])
        print(qList)
        info = zip(idList,qList,ansList)
        
        return render(request,"postAlumni.html",{'info':info})
    else:
        try:
            op = request.session['previousSearch']
            qList = []
            idList=[]
            ansList=[]
            id = -1
            for i in range(len(op)):
                if op[i]['ansTo']['id']!=id:
                    qList.append(op[i]['ansTo']['question'])
                    id=op[i]['ansTo']['id']
                    idList.append(id)
                    ansList.append(op[i]['answer'][0:100])
            info = zip(idList,qList,ansList)
            print(request.session['cachedQtn'])
            return render(request,"postAlumni.html",{'info':info})
        except:
            return render(request,"postAlumni.html")



@login_required
def alumni(request):
    try:
        getUserInfo = UserInfo.objects.filter(is_verified = True ,userType = "alumni")
    except:
        return HttpResponse("Couldnt fetch Data")

    alumniName = [f"{ppl.user.first_name} {ppl.user.last_name}" for ppl in getUserInfo]
    alumniEmail = [ppl.user.email for ppl in getUserInfo]
    img=[random.randint(1,3) for i in range(len(alumniName))]

    info = zip(alumniName,img,alumniEmail)
    return render(request,"alumni.html",{'info':info})


@csrf_exempt
def notify(request):
    if request.method == "POST":
        if request.POST['notification']:
            id = request.POST["notification"]
            usr = User.objects.filter(username = request.user).first()
            notifications = Notifications.objects.filter(user = usr,id = id)
            notifications.delete()

            notify = Notifications.objects.filter(user = usr).values()
            print(notify)
            notification = list(notify)
            
            return JsonResponse({"notify":notification},status=200)


    usr = User.objects.filter(username = request.user).first()
    notificationsObj = Notifications.objects.filter(user = usr).values()
    notifications = list(notificationsObj)
    print(usr)
    print(notifications)
    context={
        'notifications':notifications
    }
    nty = Notifications.objects.filter(user = usr)
    print(nty)
    for i in nty:
        i.is_seen = True
        i.save()
    

    return render(request,"notifications.html",{'context':context})


class AjaxNotifyView(View):
    def get(self,request):
        if request.GET.get("notification"):
            id = request.GET.get("notification")
            usr = User.objects.filter(username = request.user).first()
            notifications = Notifications.objects.filter(user = usr,id = id)
            notifications.delete()

            if request.is_ajax():
                notify = Notifications.objects.filter(user = usr,id = id).values()

                notification = list(notify)
                print("#" + notification)
                return JsonResponse({"notify":notification},status=200)

        usr = User.objects.filter(username = request.user).first()
        notifications = Notifications.objects.filter(user = usr)
        print(usr)
        print(notifications)
        context={
            'notifications':notifications
        }

        return render(request,"notifications.html",{'context':context})

def Register1(request):
    return render(request,"register1.html")

def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )

def token_send(request):
    return render(request , 'registerToken.html')
    

def Register2(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = encrypt(request.POST.get("pass"))
        fName = request.POST.get("fName")
        lName = request.POST.get("lName")
        userName = request.POST.get("userName")
        phoneNumber = request.POST.get("phoneNumber")
        userType = request.POST.get("uType")

        try:
            if User.objects.filter(username = userName).first():
                messages.success(request, 'Username is taken.')
                return redirect('/register1')

            if User.objects.filter(email = email).first():
                messages.success(request, 'Email is taken.')
                return redirect('/register1')

            user_obj = User(username = userName , email = email, first_name = fName, last_name = lName)
            user_obj.set_password(password)
            user_obj.save()

            auth_token = str(uuid.uuid4())
            info_obj = UserInfo.objects.create(user=user_obj,phoneNo=phoneNumber,userType=userType,auth_token=auth_token)
            info_obj.save()

            send_mail_after_registration(email , auth_token)
            request.session['uName'] = user_obj.username
            return redirect('/token')

        except Exception as e:
            print(e)

    return render(request,"register2.html")

def verify(request , auth_token):
    try:
        profile_obj = UserInfo.objects.filter(auth_token = auth_token).first()

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/register2')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/register2')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')

def error_page(request):
    return  render(request , 'error.html')


@login_required
def home(request):
    if request.method == "POST":
        sQuery = request.POST.get("searchInput")
        print(sQuery)
    return render(request,"postAlumni.html",abc)

def encrypt(var):
    crypt=hashlib.sha256()
    crypt.update(bytes(var,'utf-8'))
    return(crypt.hexdigest())

@login_required
def home1(request):
    try:
        query = request.session['cachedQtn']
        getGoogle = search_query(query,20)
        return render(request,"postStack.html",{'result':getGoogle})
    except:
         return render(request,"postStack.html")


@login_required
def profile(request):
    usr = User.objects.filter(username = request.user).first()
    usrInfo = UserInfo.objects.filter(user = usr).first()
    skillsToPrint = [skill.skill.skill for skill in  userSkills.objects.filter(user = usr)]
    print(skillsToPrint)
    context={
        'user':usr,
        'uInfo':usrInfo,
        'skills':skillsToPrint
    }
    return render(request,"profile.html",{'context':context})


def chatBox(request):
    return render(request,"chat.html")

def checkProfanity(comment):
    return profanity.contains_profanity(comment)

class AjaxAnsView(View):
    def get(self,request,id):
        alert = "Offensive or inappropriate language used...cant post"
        allGood = "1"
        # if request.GET.get("userPost") :
        text = request.GET.get("userPost")
        status = checkProfanity(text)
        if request.is_ajax():
            print(request)
            if(status == True):
                return JsonResponse({"Cuss":alert},status=200)
            elif(text == ""):
                return JsonResponse({"Cuss":"Blank Question cant be posted"},status=200)
            else:
                try:
                    usr = User.objects.filter(username = request.user).first()
                    qtn = Questions.objects.filter(id = id).first()
                    ans = Answers(answer = text,ansTo = qtn,author = usr)
                    ans.save()
                    return JsonResponse({"Cuss":allGood},status=200)
                except:
                    return JsonResponse({"Cuss":"couldnt upload"},status=200)
        # elif request.GET.get("ansUp"):
        #     id = request.GET.get("ansUp")
        #     if request.is_ajax():
        #         ans = Answers.objects.filter(id = id).first()
        #         ans.upVotes += 1 

        
        getQ = Questions.objects.filter(id=id)
        ansList=[ans.answer for ans in Answers.objects.filter(ansTo=getQ[0])]
        ansObj = [ans for ans in Answers.objects.filter(ansTo=getQ[0])]
        # print(ansObj)
        commentList = [comment for ans in ansObj for comment in Comments.objects.filter(commentToAnswer = ans)]
        # print(commentList)

        BigList = []
        for i in ansObj:
            BigList.append([i.answer,Comments.objects.filter(commentToAnswer = i)])
        
        # print(BigList)

    # [ [ans1, [c11, c12, ....]], [ans2, [c21, c22, ...]], ... ]

        context={
            'question':getQ[0],
            'ansObj':ansObj
        }
        


        return render(request,"answers.html",{'context':context})
    
@login_required
@csrf_exempt
def postQuestion(request):
    if request.method == "POST":
        text = request.POST.get("userPost")
        print(text)
        try:
            usr = User.objects.filter(username = request.user).first()
            qtn = Questions(question = text, userWhoAsked = usr)
            qtn.save()
            return JsonResponse({"status":200})
        except:
            return JsonResponse({"status":500})
    return render(request,"question.html")

@csrf_exempt
def save_comment(request,id):
    getA = Answers.objects.filter(id=id)
    commentList = Comments.objects.filter(commentToAnswer = getA[0])
    print(commentList)
    context = {
        'ans':getA[0].answer,
        'comments':commentList
    }

    if request.method == "POST":
        text = request.POST.get("userPost")
        print(text)

        usr = User.objects.filter(username = request.user).first()
        ans = Answers.objects.filter(id = id).first()
        com = Comments(comment = text, commentToAnswer = ans, posSentiment=True, author = usr)
        com.save()

        # new way to unpack
        comment = Comments.objects.filter(commentToAnswer = getA[0]).values()
        commentList = list(comment)

        context = {
            'ans':getA[0].answer,
            'comments':commentList
        }

        return JsonResponse({"context":context})
    else:
        getA = Answers.objects.filter(id=id)
        comment = Comments.objects.filter(commentToAnswer = getA[0]).values()
        commentList = list(comment)
        context = {
            'ans':getA[0].answer,
            'comments':commentList
        }
        return render(request,'comments.html',{'context':context})


class AjaxComView(View):
    def get(self,request,id):
        alert = "Offensive or inappropriate language used...cant post"
        allGood = "1"
        
        if not request.GET.get("isReply"):
            print("not reply")
            text = request.GET.get("userPost")
            status = checkProfanity(text)


            if request.is_ajax():
                # check sentiment
                sentiment = True if TextBlob(text).sentiment.polarity >=0 else False

                if(status == True):
                    return JsonResponse({"Cuss":alert},status=200)
                elif(text == ""):
                    return JsonResponse({"Cuss":"Blank Question cant be posted"},status=200)
                else:
                    try:
                        usr = User.objects.filter(username = request.user).first()
                        ans = Answers.objects.filter(id = id).first()
                        com = Comments(comment = text, commentToAnswer = ans, posSentiment = sentiment, author = usr)
                        com.save()
                        return JsonResponse({"Cuss":allGood},status=200)
                    except:
                        return JsonResponse({"Cuss":"couldnt upload"},status=200)
        elif request.GET.get("isReply"):
            print("reply")
            text = request.GET.get("userPost")
            print(text)
            reply = request.GET.get("isReply")
            print(reply)
            status = checkProfanity(text)

            if request.is_ajax():
                # check sentiment
                sentiment = True if TextBlob(text).sentiment.polarity >=0 else False

                if(status == True):
                    return JsonResponse({"Cuss":alert},status=200)
                elif(text == ""):
                    return JsonResponse({"Cuss":"Blank Question cant be posted"},status=200)
                else:
                    try:
                        usr = User.objects.filter(username = request.user).first()
                        ans = Answers.objects.filter(id = id).first()
                        com = Comments(replyTo = reply ,comment = text, commentToAnswer = ans, posSentiment = sentiment, author = usr)
                        com.save()
                        return JsonResponse({"Cuss":allGood},status=200)
                    except:
                        return JsonResponse({"Cuss":"couldnt upload"},status=200)



        getA = Answers.objects.filter(id=id)
        commentList = Comments.objects.filter(commentToAnswer = getA[0])
        print(commentList)
        context = {
            'ans':getA[0],
            'comments':commentList
        }
        return render(request,'comments.html',{'context':context})

def LogOut(request):
    logout(request)
    return render(request,'index.html')

def runCheck(request):
    uploaded_file = 0
    if request.method == "POST":

        base_dir = "C:/Users/Amrut/Desktop/askIt2021/finalYrRawFiles/askIt/askIt/media"
        for f in os.listdir(base_dir):
            os.remove(os.path.join(base_dir, f))

        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name,uploaded_file)
    else:
        return render(request,"register3.html")
    if(uploaded_file != 0):
        base_dir = "C:/Users/Amrut/Desktop/askIt2021/finalYrRawFiles/askIt/askIt/media"
        fileList = os.listdir(base_dir)
        print(fileList)
        image = os.path.join(base_dir,fileList[0])
        print(image)

        ans = execute(image)

        if ans == "1":
            # request.session['uName'] = "vinutha"
            user_object = User.objects.all()
            for usr in user_object:
                if usr.username == request.session['uName']:
                    userCheck = UserInfo.objects.filter(user = usr).first()
                    print(userCheck.markSheet_verified)
                    userCheck.markSheet_verified = True
                    userCheck.save()
                    print(userCheck.markSheet_verified)

            return render(request,"postAlumni.html",{"ans":"You Are All Set To Go !!"})
        elif ans == "-1":
            return render(request,"register3.html",{"err":"Make sure image is readable"})
        else:
            return render(request,"register3.html",{"err":"Uploaded document does not appear to be SFIT Marksheet"})


    # ans = execute()
    # print(ans)
    # return HttpResponse("DOne")


############################################

# TO POPULATE QnA

def populateDb(request):
    # try:
    with open('C:/Users/Amrut/Desktop/askIt2021/finalYrRawFiles/askIt/scrap/comments2.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    for j in range(2,len(data)):
        com = data[j][0]
        cTo = data[j][3]
        pos = True if data[j][4] == "TRUE" else False
        auth = data[j][5]
        reply = data[j][6]
        if reply:
            putData = User.objects.filter(email = auth)
            putA = Answers.objects.filter(answer = cTo)
            print(putA)
            pd = Comments(comment = com,commentToAnswer=putA[0],author=putData[0],posSentiment = pos,replyTo = reply)
            pd.save()
            continue
        
        putData = User.objects.filter(email = auth)
        putA = Answers.objects.filter(answer = cTo)
        pd = Comments(comment = com,commentToAnswer=putA[0],author=putData[0],posSentiment = pos)
        pd.save()
        

    return HttpResponse("status:200")
    # except:
    #     return HttpResponse("Error")


# #TO POPULATE USERS
# def populateDb(request):
#     # try:
#         # csv_path = finders.find('C:/Users/Amrut/Desktop/finalYrRawFiles/askIt/scrap/alumniData.csv')
#         with open('C:/Users/Amrut/Desktop/askIt/finalYrRawFiles/askIt/scrap/Person.csv', newline='') as f:
#             reader = csv.reader(f)
#             data = list(reader)

#         for j in range(2,len(data)):
#             email    = data[j][0]
#             password = data[j][1]
#             fullName = data[j][2]
#             userName = data[j][3]
#             phone    = data[j][4]
#             userType = data[j][5]
#             keyLink  = data[j][6]
#             print(email,password,fullName,userName,phone,userType,keyLink)   

#             pd = UserCred(email = email,password=password)
#             pd.save()
#             putData = UserInfo(fullName=fullName,userName=userName,phoneNo=phone,userType=userType, keyLink=pd)
#             putData.save()

#         return HttpResponse("status:200")
#     # except:
#     #     return HttpResponse("Error")

##############################################

def abc(request):

    return render(request,"abc.html")
##############################################


def display(request):
    name = "amrut"
    context = {
        "dynamicUserName":name
    }
    return render(request,"index.html",context)