# To run server  
python manage.py runserver

#API Testing 
http://127.0.0.1:8000/users/
example:
{
    "user_id": 1,
    "name": "siddu",
    "phone_number": "9999444400",
    "email": "siddu@gmail.com"
}

http://127.0.0.1:8000/mark_as_spam
{
    "phone_number": "1234567890"
}

http://127.0.0.1:8000/spam_count/1234567890     #this shows counts for spam phone_number

https://127.0.0.1:8000/search/siddu/    # shows name, phone_number, spam_count

https://127.0.0.1:8000/search/1234567890/    #by hitting this url can show number of spam_count for a number 



Admin credentials are:
username: siddu
password: 1234
