from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from .interaction import Markspam


class UserContact(APIView):
    authentication_classes = [BasicAuthentication]  #following basic authentication
    permission_classes = [IsAuthenticated]
    def get(self, request):
      user= User.objects.all()
      serializer = UserSerializer(user, many=True)
      return Response(serializer.data)


    def post(self,request):
       name = request.data.get('name',None)
       email = request.data.get('email',None)  
       phone_number = request.data.get('phone_number',None) 
       password = request.data.get('password', None)
       
       if not phone_number:    #if phone number is not getting shows error
            return Response({"error": "Phone number is required"}, status=400)
       
       if User.objects.filter(phone_number=phone_number).exists():   #checks if phone_number exists
            return Response({"error": "Phone number already exists"}, status=400)
       
       if email and User.objects.filter(email=email).exists():    #checks if email is exist
            return Response({"error": "email already exists"}, status=400)
       user = User(name=name, phone_number=phone_number, email=email)
       user.set_password(password)
       user.save()
       contact=Contact(user=user, phone_number=phone_number,name=name)
       contact.save()
       return Response("contact saved", status=201)

class SpamCheck(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        user_id = request.user.id
        if not phone_number:
            return Response({'error': 'Phone number is required'}, status=400)
        mark_spam = Markspam()
        mark_spam.mark_as_spam(user_id, phone_number)

        return Response({'message': 'Spam status updated for phone number'}, status=200)
    
class SpamCountView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, phone_number): 
        try:
            spam = Spam.objects.get(phone_number=phone_number)
            
            response = {'phone_number':spam.phone_number, 'spam_count':spam.count}


        except Spam.DoesNotExist:
            response = {'phone_number':phone_number, 'spam_count':0}    #if spam does not exist spam is default

        return Response(response, status=200)
    


class SearchUsingName(APIView): #search using name
    permission_classes = [IsAuthenticated]
    def get(self, request, name):
        if not name:
            return Response({'error':' Name  is required'}, status=400)
        
        exact_name_matches = User.objects.filter(name__iexact=name)  
        starting_letters_matches = User.objects.filter(name__startswith=name).exclude(name__iexact=name)
        containing_matches = User.objects.filter(name__icontains=name).exclude(name__startswith=name)

        results = list(exact_name_matches)+list(starting_letters_matches)+list(containing_matches) 
        response_data =[]
        for user in results:
            spam_likelihood = self.get_spam(user.phone_number)
            response_data.append({'name':user.name, 'phone_number':user.phone_number, 'spam':spam_likelihood})
        return Response(response_data, status=200)
    
    def get_spam(self,phone_number):
        spam = Spam.objects.filter(phone_number=phone_number).first()
        if spam:   
            return spam.count   #print spam count
        return 0
    
class SearchUsingNumber(APIView):  # Search using number
    permission_classes = [IsAuthenticated]

    def get(self, request, number):
        if not number:
            return Response({'error': 'Phone number is required'}, status=400)

        try:
            # Check if the phone number belongs to a registered user
            user = User.objects.get(phone_number=number)

            response = {'name': user.name,'phone': user.phone_number,'user': user.user_id, 'spam': self.get_spam(user.phone_number)}

            return Response(response, status=200)

        except User.DoesNotExist:
            # If not a registered user, check contacts
            contacts = Contact.objects.filter(phone_number=number)

            if contacts.exists():  # if contact exist
                response = []
                for contact in contacts:  
                    response.append({
                        'name': contact.name,
                        'phone': contact.phone_number,
                        'spam': self.get_spam_likelihood(contact.phone_number) 
                    })
                return Response(response, status=200)
            else:
                return Response({'error': 'No contact found'}, status=404)

    def get_spam(self, phone_number):
        spam = Spam.objects.filter(phone_number=phone_number).first()
        if spam:
            return spam.count
        return 0



        
        
