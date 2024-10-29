from django.contrib import admin
from .models import User, Contact, Spam

# Register your models here.\a
admin.site.register(User)
admin.site.register(Contact)
admin.site.register(Spam)
