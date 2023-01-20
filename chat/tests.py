from django.test import TestCase #Sub-Klasse "TestCase" eines Unit-Test (Isolierter Test); Klassenbasierter Ansatz statt funktionsorientiert
from django.test import Client
from django.contrib.auth.models import User
from .models import Chat, Message
from django.contrib.auth import authenticate

# Create your tests here.
#https://docs.djangoproject.com/en/4.1/topics/testing/tools/


#Testing Chat_View
# class IndexTest(TestCase):
#  def test_index(self):
#   self.client = Client() #I am Client
#   myChat = Chat.objects.get(id=1)
#   Message.objects.create(text='blablub', chat=myChat, author=self.client, receiver=self.client)
#   response = self.client.get('/chat/') #Wir speichern die Antwort der URL in der Variable response
#   self.assertEqual(response.status_code,200) #assertEqual ist eine Methode in der TestCase Klasse die den status-code der Antwort gegen den Wert 200 testet


#Testing Login_View
#Indeed, the test runner does create an instance of your test class (LoginTest) for each test method that you create. self refers to that instance.
class LoginTest(TestCase):
   def test_login(self):
    self.client = Client() #Browser-Dummy mit dem man was machen kann
    
    user = authenticate(username='tullrich', password='tullrich')
    print('Authenticated? ',user)

    response = self.client.login(username='tullrich',password='tullrich')
    print('Login? ',response)
    
    self.assertEqual(response,False) #Gibt OK zurück oder AssertionError: X != Y


