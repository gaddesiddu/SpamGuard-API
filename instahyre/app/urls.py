from django.urls import path
from .views import UserContact, SpamCheck, SpamCountView, SearchUsingName, SearchUsingNumber

urlpatterns = [
    path('users/', UserContact.as_view(), name='user-contact'),  # This will handle both GET and POST requests
    path('mark_as_spam/', SpamCheck.as_view(), name='mark_spam'),  #this url used to mark number to spam
    path('spam_count/<str:phone_number>/', SpamCountView.as_view(), name='spam_count'), #to increase spam count
    path('search/<str:name>/', SearchUsingName.as_view(), name="seach_by_name"),  #search using name
    path('search/number/<str:number>/', SearchUsingNumber.as_view(), name="seach_by_number"),  #search using number

]
