from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .models import Chat, Message
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import JsonResponse
from django.core import serializers


# Create your views here.

@login_required(login_url='/login/') #index is only accessible if logged in, otherwise you will get redirected to login
def index(request):
    """
    This is a view to render the chat
    """
    if request.method == 'POST':
     myChat = Chat.objects.get(id=1) #Get Chat with id=1
     new_message = Message.objects.create(text=request.POST['textmessage'], chat=myChat, author=request.user, receiver=request.user) #Writes into our Message-Model
     serialized_obj = serializers.serialize('json',[new_message], use_natural_foreign_keys=True) #Foreign-Keys are displayed as text
     return JsonResponse(serialized_obj[1:-1],safe=False) #returns JSON
     
    #If GET 
    chatMessages = Message.objects.filter(chat__id=1) #Get all messages from Chat with id=1
    return render(request, 'chat/index.html', {'messages': chatMessages})


def login_view(request):
    """
     This is a view to login the user if not logged in, otherwise redirects to Chat-HTML
    """
    redirect = request.GET.get('next') #Variable redirect gets value of next-parameter, for redireciting to /chat/
    
    if request.method == 'POST':
       user = authenticate(username=request.POST.get('username'), password=request.POST.get('password')) #Authentification of User possible?
       if user != 'None': 
           #User authenticated/registered (username & password are correct)
           login(request,user) #Logs in the User
           return JsonResponse({"LoggedIn": True, "RedirectTo": '/chat/'})
       else: 
           #User not authenticated/registered (username or password is not correct)
           return JsonResponse({"LoggedIn": False, "RedirectTo": '/chat/'})

    return render(request, 'auth/login.html',{'redirect': redirect}) #GET-Request


def register_view(request):
 """
  This is a view to register the user. It generates a 500 Server Error if user alreasy exists
 """
 if request.method == 'POST' and request.POST.get('password1') == request.POST.get('password2'):
   username=request.POST.get('username')
   password1=request.POST.get('password1')
   createduser = User.objects.create_user(username=username,password=password1) #User is created -> Error if user exists
   createduser = User.objects.filter(username=createduser) #Filters the created user -> Error if user exists
   
   serialized_obj = serializers.serialize('json',createduser)
   return JsonResponse(serialized_obj[1:-1],safe=False) #returns JSON

 return render(request, 'register/register.html') #GET-Request


def logout_view(request):
 """
 This is a view to logout the user if logged in, otherwise redirects to Login-HTML
 """
 if request.user.is_authenticated:
   logout(request)
   textforuser = 'Logged out successfully. Thanks for chatting ;)'
 else:
   return HttpResponseRedirect('/chat/')

 return render(request, 'logout/logout.html',{'textforuser': textforuser})

