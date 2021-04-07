from django.shortcuts import render, HttpResponse
from .crawler import getPosts
from better_profanity import profanity
from django.views.generic import View
from django.http import JsonResponse
import hashlib
import pyrebase
import random


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
        email = request.POST.get("email")
        password = request.POST.get("pass")
        try:
            user = auth.sign_in_with_email_and_password(email,password)
        except:
            message = " Incorrect email or password"
            return render(request,"login.html",{"alertMessage":message})

    qId=database.child('Questions').shallow().get().val()
    lst_qts = []
    for i in qId:
        lst_qts.append(i)

    all_qts = []
    for i in lst_qts:
        qts = database.child('Questions').child(i).child('Question_asked').get().val()
        all_qts.append(qts)
    
    personAsked = []
    for i in lst_qts:
        ppl = database.child('Questions').child(i).child('first_name').get().val()
        personAsked.append(ppl)

    
    comb_lst = zip(personAsked,all_qts)
    
    return render(request,"postAlumni.html",{'comb_lst':comb_lst})

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

def chatBox(request):
    return render(request,"chat.html")

def checkProfanity(comment):
    return profanity.contains_profanity(comment)

def ans(request):
    return render(request,"answers.html")




############################################
def abc(request):
    return render(request,"abc.html")
##############################################