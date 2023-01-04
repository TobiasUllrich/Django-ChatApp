from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .models import Chat, Message

# Create your views here.
def index(request):
    if request.method == 'POST':
     print ("Received data" + request.POST['textmessage']) #Gibt uns die Nachricht aus, falls es sich um eine POST-Methode handelt
     myChat = Chat.objects.get(id=1) #Zieht uns den Chat mit der ID 1 und dieses Objekt wird unten mit der Message-Tabelle verknüpft
     Message.objects.create(text=request.POST['textmessage'], chat=myChat, author=request.user, receiver=request.user) #Erstellt einen Datenbankeintrag und füllt die Felder

    #Unteres wird immer ausgeführt 
    chatMessages = Message.objects.filter(chat__id=1) #Wir holen uns alle Nachrichten in eine Variable wo die Chat-ID = 1 ist; Einrücken, weil es in jedem Fall angezeigt werden soll (nicht in den If-Teil packen)!
    return render(request, 'chat/index.html', {'messages': chatMessages}) #Gibt uns etwas zurück


def login_view(request):
    #Wenn POST-Methode, dann wird der If-Block ausgeführt
    if request.method == 'POST':
       user = authenticate(username=request.POST.get('username'), password=request.POST.get('password')) #Authentifizierungs-Funktion von Django
       if user:
           login(request,user) #Login-Funktion von Django -> loggt den User ein, wenn Username+Passwort korrekt sind
           return HttpResponseRedirect('/chat/') #Weiterleitung zum chat
       else:
           return render(request,'auth/login.html', {'wrongPassword': True})

    return render(request, 'auth/login.html')