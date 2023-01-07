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
     serialized_obj = serializers.serialize('json',[new_message])
     return JsonResponse(serialized_obj[1:-1],safe=False) #Gibt uns einen Array zurück, weswegen wir vorher die [] wegschneiden
     
    #Unteres wird NICHT immer ausgeführt, sondern nur wenn es kein POST-Request ist, weil bei POST springt er vorher raus durch return 
    print('GET-Request')
    chatMessages = Message.objects.filter(chat__id=1) #Wir holen uns alle Nachrichten in eine Variable wo die Chat-ID = 1 ist; Einrücken, weil es in jedem Fall angezeigt werden soll (nicht in den If-Teil packen)!
    return render(request, 'chat/index.html', {'messages': chatMessages}) #Sendet Daten ans HTML zurück


def login_view(request):
    redirect=request.GET.get('next') #Variable redirect erhält den Wert (/chat/) unseres Qry-Parameters oben aus der URL-Leiste, sobald wir uns einloggen wollen
    print('GET-REQUEST NEXT',request.GET.get('next'))
    print('POST-REQUEST NEXT',request.POST.get('next'))
    print('GET-REQUEST redirect',request.GET.get('redirect'))
    print('POST-REQUEST redirect',request.POST.get('redirect'))
    #Wenn POST-Methode, dann wird der If-Block ausgeführt
    if request.method == 'POST':
       user = authenticate(username=request.POST.get('username'), password=request.POST.get('password')) #Authentifizierungs-Funktion von Django
       if user:
           login(request,user) #Login-Funktion von Django -> loggt den User ein, wenn Username+Passwort korrekt sind
           return HttpResponseRedirect(request.POST.get('redirect')) #Weiterleitung zur URL, welche in unserer redirect Variable gespeichert ist
       else:
           return HttpResponseRedirect('/chat/')

    return render(request, 'auth/login.html',{'redirect': redirect}) #redirect-Variable zeigt an wohin wir weiterleiten





def register_view(request):
 print('Registerbereich aufgerufen')
 #Checken ob user existiert
 #Checken ob passwörter gleich
 usercreated=False
 textforuser='Just type in your wished username and your password'

 if request.method == 'POST':
   username=request.POST.get('username')
   password1=request.POST.get('password1')
   password2=request.POST.get('password2')
   #If user does not already exist and passwords are equal -> User is created
   if not User.objects.filter(username=username).exists() and password1==password2:
    User.objects.create_user(username=username,password=password1)
    usercreated=True
    textforuser='Congratulations. You are registered :)'
   elif User.objects.filter(username=username).exists():
    usercreated=False
    textforuser='We are sorry. This username already exists. Please choose another one.'
   else:
    usercreated=False
    textforuser='We are sorry. Your passwords differ. Please ensure they are equal.'

 return render(request, 'register/register.html',{'usercreated': usercreated,'textforuser': textforuser})


def logout_view(request):

 if request.user.is_authenticated:
   logout(request)
   textforuser = 'You have been logged out successfully.'
 else:
   textforuser = 'Can`t logout, because you are not logged in.'

 return render(request, 'logout/logout.html',{'textforuser': textforuser})

