from django.test import TestCase #Sub-Klasse "TestCase" eines Unit-Test (Isolierter Test); Klassenbasierter Ansatz statt funktionsorientiert
from django.test import Client
from django.contrib.auth.models import User
from .models import Chat, Message

# Create your tests here.
#https://docs.djangoproject.com/en/4.1/topics/testing/tools/


#Testing Chat_View
class IndexTest(TestCase):
 def test_index(self):
  self.client = Client() #I am Client
  myChat = Chat.objects.get(id=1)
  Message.objects.create(text='blablub', chat=myChat, author=self.client, receiver=self.client)
  response = self.client.get('/chat/') #Wir speichern die Antwort der URL in der Variable response
  self.assertEqual(response.status_code,200) #assertEqual ist eine Methode in der TestCase Klasse die den status-code der Antwort gegen den Wert 200 testet


#Testing Login_View
class LoginTest(TestCase):
   def test_login(self):
    self.client = Client()
    self.user = User.objects.create_user('test_user',password='test_user')
    self.client.login(username='test_user',password='test_user')
    response = self.client.get('/login/')
    self.assertEqual(response.status_code,200)