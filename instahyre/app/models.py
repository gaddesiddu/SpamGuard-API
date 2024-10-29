from django.db import models
from django.contrib.auth.hashers import make_password, check_password



class User(models.Model):   #User model
    user_id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone_number=models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True,null=True, blank=True)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    def set_password(self, raw_password):    #password is encrypted
        self.password= make_password(raw_password)
    def check_password(self, raw_password):   #checking password is matching  
        return check_password(raw_password, self.password)
    
    
class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10)
    name = models.CharField(max_length=100)


    def __str__(self):
        return f'{self.name} {self.phone_number}'
    

class Spam(models.Model):
    phone_number = models.CharField(max_length=10, primary_key=True)
    count = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.phone_number} - Spam Count: {self.count}'   #shows spam count in admin panel

