#Sub-Klasse "TestCase" eines Unit-Tests (Isolierter Test); Klassenbasierter Ansatz statt funktionsorientiert
#The Test runner does create an instance of your test class (LoginTest) for each test method that you create. self refers to that instance.
from django.test import TestCase 
from django.test import Client
from django.contrib.auth.models import User
from .models import Chat, Message
from django.contrib.auth import authenticate
from django.contrib import auth
from datetime import date


# Create your tests here.
#https://docs.djangoproject.com/en/4.1/topics/testing/tools/
#https://docs.djangoproject.com/en/4.1/topics/testing/advanced/


#Testing Chat_View
class IndexTest(TestCase):
 def test_index(self):
  
  self.client = Client() #I am Client (Browser-Dummy)
  test_login(self) 
  myChat = Chat.objects.create() #Creates an empty Entry in the Model Chat and therefore also the Model Chat itself
  myMessage = Message.objects.create() #Creates an empty Entry in the Model Message and therefore also the Model Message itself
  response = self.client.post('/chat/', {'textmessage': 'hallo', 'author': self.client, 'receiver': self.client}) #Wir speichern die Antwort der URL in der Variable response (null=True in Models setzen, falls Fehler erzeugt wird)
  print('Response from Server ',response) #RESPONSE 200
  print('Messages ',Message.objects.all(),' and Chats ',Chat.objects.all()) #Now we have TWO MESSAGES and ONE CHAT

  print(Message.objects.filter(text='hallo',chat=1,author=1,receiver=1)) #Geht
  print(Chat.objects.filter(id=1)[0]) #Geht
  
  self.assertEqual(response.status_code,200) #assertEqual ist eine Methode in der TestCase Klasse die den status-code der Antwort gegen den Wert 200 testet

#Login-Funktion
def test_login(self):    
    #User with Password has to be created at first, to make login
    user = User.objects.create(username='testuser')
    user.set_password('12345')
    user.save()

    self.client = Client() #I am Client (Browser-Dummy)
    response = self.client.login(username='testuser', password='12345')
    print('Als welcher User ist unser Client eingeloggt?',auth.get_user(self.client))
    print('Ist unser Client überhaupt eingeloggt?',auth.get_user(self.client).is_authenticated)
    
    self.assertEqual(response,True) #Gibt OK zurück oder AssertionError: X != Y
    assert auth.get_user(self.client).is_authenticated #Prüft wir uns eingeloggt haben mit den Daten von oben


#FUNKTIONIERT
#Testing Login_View
class LoginTest(TestCase):
   def test_login(self):    
    #User with Password has to be created at first, to make login
    user = User.objects.create(username='testuser')
    user.set_password('12345')
    user.save()

    self.client = Client() #I am Client (Browser-Dummy)
    response = self.client.login(username='testuser', password='12345')
    print('Als welcher User ist unser Client eingeloggt?',auth.get_user(self.client))
    print('Ist unser Client überhaupt eingeloggt?',auth.get_user(self.client).is_authenticated)
    
    self.assertEqual(response,True) #Gibt OK zurück oder AssertionError: X != Y
    assert auth.get_user(self.client).is_authenticated #Prüft wir uns eingeloggt haben mit den Daten von oben

#FUNKTIONIERT
#Testing Register_View
class RegisterTest(TestCase):

   def test_register(self):    

    self.client = Client() #I am Client (Browser-Dummy)
    response = self.client.post('/register/', {'username': 'testuser', 'password1':'TU*+?12345', 'password2':'TU*+?12345'}) #Wir speichern die Antwort der URL in der Variable response
    print('Antwort des POST-Requests ',response)
    getRegisteredUserViaUsername = User.objects.get(username='testuser') #If User created with username 'testuser'
    print('Registrierter User ', getRegisteredUserViaUsername)
    getRegisteredUserViaId = User.objects.get(id=1) #If User created it must have id=1
    print('ID Registrierter User ', getRegisteredUserViaId)

    self.assertEqual(getRegisteredUserViaUsername, getRegisteredUserViaId) #Prüft ob unser registrierte User die id=1 hat


#FUNKTIONIERT
#Testing Logout_View
class LogoutTest(TestCase):
   def test_logout(self):
     #Login-First
     test_login(self)
     # Log-Out
     self.client.logout()
     print('Ist unser Client ausgeloggt?', auth.get_user(self.client).is_authenticated)
     assert not auth.get_user(self.client).is_authenticated #Prüft ob das Ausloggen geklappt hat

#Login-Funktion
def test_login(self):    
    #User with Password has to be created at first, to make login
    user = User.objects.create(username='testuser')
    user.set_password('12345')
    user.save()

    self.client = Client() #I am Client (Browser-Dummy)
    response = self.client.login(username='testuser', password='12345')
    print('Als welcher User ist unser Client eingeloggt?',auth.get_user(self.client))
    print('Ist unser Client überhaupt eingeloggt?',auth.get_user(self.client).is_authenticated)
    
    self.assertEqual(response,True) #Gibt OK zurück oder AssertionError: X != Y
    assert auth.get_user(self.client).is_authenticated #Prüft wir uns eingeloggt haben mit den Daten von oben

