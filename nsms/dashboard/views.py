from django.shortcuts import render

def home(request):
    return render(request, 'dashboard/dashboard.html')  # تأكد من وجود ملف home.html



#python manage.py runserver