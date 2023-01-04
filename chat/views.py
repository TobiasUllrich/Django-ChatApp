from django.shortcuts import render
from .models import Chat, Message

# Create your views here.
def index(request):
    if request.method == 'POST':
     print ("Received data" + request.POST['textmessage']) #Gibt uns die Nachricht aus, falls es sich um eine POST-Methode handelt
     myChat = Chat.objects.get(id=1) #Zieht uns den Chat mit der ID 1 und dieses Objekt wird unten mit der Message-Tabelle verknüpft
     Message.objects.create(text=request.POST['textmessage'], chat=myChat, author=request.user, receiver=request.user) #Erstellt einen Datenbankeintrag und füllt die Felder
     chatMessages = Message.objects.filter(chat__id=1) #Wir holen uns alle Nachrichten in eine Variable wo die Chat-ID = 1 ist
    return render(request, 'chat/index.html', {'messages': chatMessages}) #Gibt uns etwas zurück