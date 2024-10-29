from .models import Spam

class Storage:
    def get_spam_by_phone_number(self, phone_number):
        return Spam.objects.filter(phone_number=phone_number)
    
    def update_spam_count_phone_number(self,phone_number):
        spam = Spam.objects.get(phone_number=phone_number)
        spam.count+=1
        spam.save()

    def create_new_spam_to_phone_number(self, phone_number):
        Spam.objects.create(phone_number=phone_number, count=1)
        