#Sub-Klasse "TestCase" eines Unit-Tests (Isolierter Test); Klassenbasierter Ansatz statt funktionsorientiert
#The Test runner does create an instance of your test class (LoginTest) for each test method that you create. self refers to that instance.
from django.test import TestCase 
from django.test import Client
from django.contrib.auth.models import User
from .models import Chat, Message
from django.contrib.auth import authenticate
from django.contrib import auth


# Create your tests here.
#https://docs.djangoproject.com/en/4.1/topics/testing/tools/
#https://docs.djangoproject.com/en/4.1/topics/testing/advanced/


#Testing Chat_View
# class IndexTest(TestCase):
#  def test_index(self):
#   self.client = Client() #I am Client (Browser-Dummy)
#   myChat = Chat.objects.create() #Model Chat has to be created, because not existing, when Testing
#   myMessage = Message.objects.create() #Model Message has to be created, because not existing, when Testing
#   response = self.client.post('/chat/', {'textmessage': 'hallo', 'author':self.client, 'receiver':self.client}) #Wir speichern die Antwort der URL in der Variable response (null=True in Models setzen, falls Fehler erzeugt wird)
#   print(response) #RESPONSE 302!!!
#   getPostedMessage = Message.objects.get(id=1) #If Message created it is the first Message
#   self.assertEqual(getPostedMessage.chat,myChat.id)
#   self.assertEqual(getPostedMessage.text,"hallo")
#   self.assertEqual(getPostedMessage.author,self.client)
#   self.assertEqual(response.status_code,200) #assertEqual ist eine Methode in der TestCase Klasse die den status-code der Antwort gegen den Wert 200 testet


#Testing Login_View
class LoginTest(TestCase):
   def test_login(self):    
    #User with Password has to be created at first, to make login
    user = User.objects.create(username='testuser')
    user.set_password('12345')
    user.save()

    self.client = Client() #I am Client (Browser-Dummy)
    response = self.client.login(username='testuser', password='12345')
    self.assertEqual(response,True) #Gibt OK zurück oder AssertionError: X != Y


#Testing Register_View
class RegisterTest(TestCase):
   def test_register(self):    

    self.client = Client() #I am Client (Browser-Dummy)
    response = self.client.post('/register/', {'username': 'testuser', 'password1':'12345', 'password2':'12345'}) #Wir speichern die Antwort der URL in der Variable response
    print('Antwort des POST-Requests ',response)

    #getUser = User.objects.get(username='testuser') #If User created with username 'testuser'
    print('Registrierter User ', auth.get_user(self.client))
    print('Registrierter User ', response.wsgi_request.user)


    assert auth.get_user(self.client).is_authenticated
    #self.assertEqual(getUser, 1)
    self.assertEqual(response.status_code, 200) #Gibt OK zurück oder AssertionError: X != Y