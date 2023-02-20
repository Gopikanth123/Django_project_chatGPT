from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
import openai
from .models import Query
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.forms import UserCreationForm



def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user=auth.authenticate(username=username,password=password)
        
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Invalid credentials')
            return redirect('login')
    else:
        return render(request,'login.html')



def logout(request):
    auth.logout(request)
    return redirect('/')


def register(request):
    if request.method == 'POST':
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'username already exists')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'email already exists')
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,password=password1,email=email)
                user.save()
                messages.info(request,"user created")
        else:
            messages.info(request,"password not matching...")
            return redirect('register')
        return redirect('/')
    else:
         return render(request,'registration.html')


# Create your views here.
def home(request):
    # data=Query.objects.all()
    
    return render(request,'home.html')


def chat(request):
    inp=request.POST["message"]
    openai.api_key=""
    response = openai.Completion.create(
     model="text-davinci-003",
     prompt=inp,
     temperature=0.9,
     max_tokens=150,
     top_p=1,
     frequency_penalty=0.0,
     presence_penalty=0.6,
     stop=[" Human:", " AI:"]
    )
    res=response['choices'][0]['text']
    # data=Query.objects.all()

    return render(request,'home.html', {'response':res})


# def generate_response(inp):
#     openai.api_key="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"
#     response = openai.Completion.create(
#      model="text-davinci-003",
#      prompt=inp,
#      temperature=0.9,
#      max_tokens=150,
#      top_p=1,
#      frequency_penalty=0.0,
#      presence_penalty=0.6,
#      stop=[" Human:", " AI:"]
#     )
#     return response['choices'][0]['text']

# @login_required
# def home(request):
#     if request.method == 'POST':
#         message = request.POST['message']
#         response = generate_response(message)
#         Query.objects.create(user=request.user, question=message, answer=response)
#     else:
#         response = ''
#     data = Query.objects.filter(user=request.user)
#     return render(request, 'home.html', {'data': data, 'response': response})
