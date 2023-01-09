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
@login_required(login_url='/login/') #Falls man nicht eingeloggt ist wird man sofort zum Login weitergeleitet
def index(request):
    """
    This is a view to render the chat html
    """
    if request.method == 'POST':
     print ("Received data" + request.POST['textmessage']) #Gibt uns die Nachricht aus, falls es sich um eine POST-Methode handelt
     print ("Received data" + request.POST.get('textmessage')) #Gibt uns die Nachricht aus, falls es sich um eine POST-Methode handelt
     myChat = Chat.objects.get(id=1) #Zieht uns den Chat mit der ID 1 und dieses Objekt wird unten mit der Message-Tabelle verknüpft
     new_message = Message.objects.create(text=request.POST['textmessage'], chat=myChat, author=request.user, receiver=request.user) #Erstellt einen Datenbankeintrag und füllt die Felder
     serialized_obj = serializers.serialize('json',[new_message], use_natural_foreign_keys=True)
     return JsonResponse(serialized_obj[1:-1],safe=False) #Gibt uns einen Array zurück, weswegen wir vorher die [] wegschneiden
     
    #Unteres wird NICHT immer ausgeführt, sondern nur wenn es kein POST-Request ist, weil bei POST springt er vorher raus durch return 
    print('GET-Request')
    chatMessages = Message.objects.filter(chat__id=1) #Wir holen uns alle Nachrichten in eine Variable wo die Chat-ID = 1 ist; Einrücken, weil es in jedem Fall angezeigt werden soll (nicht in den If-Teil packen)!
    return render(request, 'chat/index.html', {'messages': chatMessages}) #Sendet Daten ans HTML zurück


def login_view(request):
    redirect=request.GET.get('next') #Variable redirect get value of next-parameter
 
    if request.method == 'POST': #POST-Request
       user = authenticate(username=request.POST.get('username'), password=request.POST.get('password')) #Authentification of User-Data
       login(request,user) #Logs in the User if authenticated (username & password are correct)
       if user: #Success
           return JsonResponse({"LoggedIn": True, "RedirectTo": '/chat/'})
       else: #Fail
           return JsonResponse({"LoggedIn": False})

    return render(request, 'auth/login.html',{'redirect': redirect}) #GET-Request





def register_view(request):
 print('Registerbereich aufgerufen')

 if request.method == 'POST' and request.POST.get('password1') == request.POST.get('password2'):
   username=request.POST.get('username')
   password1=request.POST.get('password1')
   createduser = User.objects.create_user(username=username,password=password1)

   createduser = User.objects.filter(username=createduser)
   print('yyyyyyyyyyyyyyyyyyyyyy',createduser)

   serialized_obj = serializers.serialize('json',createduser)
   print('xxxxxxxxxxxxxxxxxxxxx',serialized_obj)
   return JsonResponse(serialized_obj[1:-1],safe=False) #Gibt uns einen Array zurück, weswegen wir vorher die [] wegschneiden
   #return JsonResponse({"Registered": User.objects.filter(username=createduser)})

 return render(request, 'register/register.html')



def logout_view(request):

 if request.user.is_authenticated:
   logout(request)
   textforuser = 'Logged out successfully. Thanks for chatting ;)'
 else:
   return HttpResponseRedirect('/chat/')

 return render(request, 'logout/logout.html',{'textforuser': textforuser})

