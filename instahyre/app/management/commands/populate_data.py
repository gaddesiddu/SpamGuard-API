import random
from django.core.management.base import BaseCommand
from app.models import User, Contact, Spam  # from app.models imported model_name 
from faker import Faker    # it takes realistic looking data like name,phone_number, email

fake = Faker()

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        # TO Create sample Users
        for _ in range(50):  # Creating 50 users
            user = User.objects.create(
                name=fake.name(),
                phone_number=fake.phone_number()[-10:],  # phone_number max_length=10
                email=fake.email(),
                password='password123'  
            )

            # Created some Contacts for each user
            for _ in range(random.randint(1, 5)):  # Each user can have 1 to 5 contacts
                Contact.objects.create(
                    user=user,
                    phone_number=fake.phone_number()[-10:],  # Again, 10-digit phone_number because phone_number max_length=10
                    name=fake.name()
                )

        # To Create some Spam entries
        for _ in range(20):  # Create 20 spam entries
            phone_number = fake.phone_number()[-10:]  #10-digit phone_number
            Spam.objects.create(
                phone_number=phone_number,
                count=random.randint(1, 10) 
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with sample data'))
