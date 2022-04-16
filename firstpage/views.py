from django.contrib.auth.models import User,auth
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate
from .models import connect,catagory,prediction,extra_features
import numpy as np
import pandas as pd 



# Create your views here.
def home(request):
    return render(request,'index.html')
def login(request):
    return render(request,'login.html')
def aboutus(request):
    return render(request,'aboutus.html')
def register(request):
    return render(request,'register.html')

def newmember(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        username=request.POST['email']
        if password==confirm_password :
            if  User.objects.filter(username=username).exists()==True:
                 messages.info(request,'email has already registered')
                 return redirect('register.html')
            else:
                user=User.objects.create_user(username=username,last_name=last_name,email=email,first_name=first_name,password=password)
                user.save();
                print('sucess')
                return redirect('login.html')
        else:
            messages.info(request,'password not matching')
            return redirect('register.html')


    else :
        return HttpResponse('SOMETHING WENT WRONG')


def newlogin(request):
    if request.method=='POST':
        email_acquired=request.POST['emailid']
        password_acquired=request.POST['password']
        print(email_acquired)
        print(password_acquired)
        user=authenticate(username = email_acquired, password = password_acquired)
        
        if user is not None:
            auth.login(request,user)
            return redirect("question.html")
        else:
            messages.info(request,'Incorrect username or password')
            return redirect("login.html")

    else:
        
       return redirect('login.html')

def question(request):
    return render(request,'question.html')

def logout(request):
    auth.logout(request)
    return redirect('index.html')
def hey(request):
    dests=connect.objects.all()
    print(dests)
    return render(request,"hey.html",{'dests':dests})


def predict(request):
    if request.method=='POST':
        user_choice = request.POST['catagory_selection'] 
        obj=catagory()
        response=obj.cat(user_choice)#this holds the all the symptoms of the selected disease
        symptoms=[]
        for i in range(len(response)):
            symptoms.append((response[i],i))
        out=len(symptoms)
        return render(request,"symptoms.html",{'dests':symptoms})  #symptoms consiset of [[symptom_name,1]]




def result_prediction(request):
    length=len(request.POST)#returns a dictionary
    print(type(request.POST))
    print(request.POST)
    #print(length)
    user_choice=[]
    for symp in range(0,length-1):
        symp=request.POST[str(symp)]
        user_choice.append(symp)
    #print(user_choice)
    print(len(user_choice))
    #print(type(user_choice))
    user_inputs=np.array(user_choice).reshape(1,len(user_choice))
    user_inputs=pd.DataFrame(user_inputs)
    
    
    #creating path for prediction class
    user_choice=list(map(int,user_choice)) # this line changes string to integer
    print(user_choice,len(user_choice))
    pred=prediction()

    if sum(user_choice)==0:
        testers=['You are healthy']
        result=""

    elif sum(user_choice)==len(user_choice):
        testers=['I think you have all disease in this world']
        result=""

    elif len(user_choice)==22:#skin disease
        result=pred.skin_predict_model(user_inputs)

    elif len(user_choice)==28:#eye disease
        result=pred.eye_predict_model(user_inputs)

    elif len(user_choice)==52:#general disease
        result=pred.general_predict_model(user_inputs)
    else :
        pass

    if result !="" or None:

        print(result)
        #print(list(result)[0])
        additional=extra_features()
        desc,hosp,contact,addr = additional.disp(list(result)[0])
        
        print(desc[0],hosp[0],contact[0],addr[0])

        resultt=[f'Prediction : {result[0]}',f'Description : {desc[0]}',f'Hospital : {hosp[0]}',f' {addr[0]}',f'{contact[0]}']


        return render(request,"result.html",{'dests':resultt})  #symptoms consiset of [[symptom_name,1]]
    else:
        print(testers)
        resultt=testers
        return render(request,"result.html",{'dests':resultt})  #symptoms consiset of [[symptom_name,1]]