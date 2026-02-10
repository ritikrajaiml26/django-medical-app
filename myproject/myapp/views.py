from django.shortcuts import render
from django.http import HttpResponse ,HttpRequest

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib import messages
import re





# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def home (request):
    return render(request,'home.html')





'''def register(request):
    if request.method == "POST":

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        context = {}

        # EMAIL FORMAT CHECK
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            context['email_error'] = "Enter a valid email address"

        # PASSWORD MATCH
        if password != confirm_password:
            context['password_error'] = "Passwords do not match"

        # DUPLICATE EMAIL
        if User.objects.filter(email=email).exists():
            context['email_error'] = "Email already exists"

        if context:
            return render(request, 'register.html', context)
'''

import re
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

def register(request):
    if request.method == "POST":

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        context = {}

        # EMAIL FORMAT CHECK
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            context['email_error'] = "Enter a valid email address"

        # PASSWORD MATCH
        if password != confirm_password:
            context['password_error'] = "Passwords do not match"

        # DUPLICATE EMAIL
        if User.objects.filter(email=email).exists():
            context['email_error'] = "Email already exists"

        # AGAR ERROR HAI
        if context:
            return render(request, 'register.html', context)

        # USER CREATE
        User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        return redirect('login')

    # GET REQUEST
    return render(request, 'register.html')










def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "login.html", {
                "error": "Invalid Email or Password"
            })

    return render(request, "login.html")






def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard.html')
    return redirect('login')


def user_logout(request):
    logout(request)
    return redirect('login')



@api_view(['POST'])
def api_register(request):
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    username = request.data.get('username')
    password = request.data.get('password')

    if User.objects.filter(username=username).exists():
        return Response({'status': 'user exists'})

    User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name
    )

    return Response({'status': 'registered'})



@api_view(['POST'])
def api_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        return Response({'status': 'success'})
    return Response({'status': 'failed'})

from django.contrib.auth import logout

@api_view(['POST'])
def api_logout(request):
    logout(request)
    return Response({'status': 'logged out'})

@api_view(['POST'])
def api_reset_password(request):
    username = request.data.get('username')
    new_password = request.data.get('new_password')

    try:
        user = User.objects.get(username=username)
        user.set_password(new_password)
        user.save()
        return Response({'status': 'password updated'})
    except User.DoesNotExist:
        return Response({'status': 'user not found'})



from .models import Reminder

def dashboard(request):
    if request.user.is_authenticated:
        reminders = Reminder.objects.filter(user=request.user)
        return render(request, 'dashboard.html', {'reminders': reminders})
    return redirect('login')


def add_reminder(request):
    if request.method == "POST":
        med = request.POST.get('medicine')
        date = request.POST.get('date')
        time = request.POST.get('time')
        note = request.POST.get('note')

        Reminder.objects.create(
            user=request.user,
            medicine=med,
            date=date,
            time=time,
            note=note
        )

        return redirect('dashboard')

    return render(request, 'add_reminder.html')




def delete_reminder(request, id):
    Reminder.objects.get(id=id).delete()
    return redirect('dashboard')

def mark_taken(request, id):
    r = Reminder.objects.get(id=id)
    r.status = True
    r.save()
    return redirect('dashboard')

def edit_reminder(request, id):
    r = Reminder.objects.get(id=id)

    if request.method == "POST":
        r.medicine = request.POST.get('medicine')
        r.date = request.POST.get('date')
        r.time = request.POST.get('time')
        r.note = request.POST.get('note')

        r.status = False  

        r.save()

    return redirect('dashboard')





from .models import Profile

def profile_view(request):

    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        profile.note = request.POST.get('note')

        if request.FILES.get('photo'):
            profile.photo = request.FILES.get('photo')

        profile.save()

    return render(request, 'profile.html', {'profile': profile})


from .models import Profile

def dashboard(request):

    Profile.objects.get_or_create(user=request.user)

    reminders = Reminder.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'reminders': reminders})








#api 

@api_view(['POST'])
def api_add_reminder(request):
    user = request.user
    medicine = request.data.get('medicine')
    date = request.data.get('date')
    time = request.data.get('time')
    note = request.data.get('note')

    Reminder.objects.create(
        user=user,
        medicine=medicine,
        date=date,
        time=time,
        note=note
    )

    return Response({'status': 'added'})



@api_view(['GET'])
def api_reminders(request):
    user = request.user
    data = Reminder.objects.filter(user=user).values()
    return Response(data)


@api_view(['POST'])
def api_delete(request, id):
    Reminder.objects.filter(id=id).delete()
    return Response({'status': 'deleted'})


@api_view(['POST'])
def api_taken(request, id):
    r = Reminder.objects.get(id=id)
    r.status = True
    r.save()
    return Response({'status': 'taken'})


@api_view(['GET'])
def api_profile(request):
    p = Profile.objects.get(user=request.user)
    return Response({
        'name': request.user.first_name,
        'email': request.user.email,
        'note': p.note
    })


@api_view(['GET'])
def api_profile(request):
    p = Profile.objects.get(user=request.user)
    return Response({
        'name': request.user.first_name,
        'email': request.user.email,
        'note': p.note
    })

@api_view(['POST'])
def api_profile_update(request):
    p = Profile.objects.get(user=request.user)
    p.note = request.data.get('note')
    p.save()
    return Response({'status': 'updated'})


