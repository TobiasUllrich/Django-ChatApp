from django.contrib import admin
from .models import Chat, Message


class MessageAdmin(admin.ModelAdmin):
   fields = ('chat','text','created_at', 'author', 'receiver') #Diese Felder werden angezeigt
   list_display = ('created_at', 'author', 'text', 'receiver') #Zeigt die Felder in Reihenfolge schön nebeneinander an
   search_fields = ('text',) #Fertiger Filter für das Feld-Text

# Register your models here.
admin.site.register(Message, MessageAdmin)
admin.site.register(Chat)