from django.db import models
from datetime import date
from django.conf import settings

#Create your models here.


# Neue Klasse die quasi einer Datenbank-Tabelle entspricht
class Chat(models.Model):
    created_at = models.DateField(default=date.today)


class AuthorReceiverManager(models.Manager):
    def get_by_natural_key(self, author, receiver):
        return self.get(au=author, re=receiver)


# Neue Klasse die quasi einer Datenbank-Tabelle entspricht
class Message(models.Model):
    #Text-Feld & Datums-Feld
    text = models.CharField(max_length=500)
    created_at = models.DateField(default=date.today)  

#chat = Chat Klasse verknüpfen

#Verknüpfung mit Fremdschlüssel des aktuell registrierten Users 
# + Wenn User gelöscht, dann auch der Chat (CASCADE)
# + Beziehungsschlüssel = Attribut author im Objekt Message
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_message_set',null=True) 
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver_message_set',null=True) 

#Standarwert einer Nachricht ist Null (default=None) und wir können auch nix mitgeben (blank=True) und Datenbank akzeptiert Null-Werte (null=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat_message_set', default=None, blank=True, null=True) 
    
    objects = AuthorReceiverManager()


