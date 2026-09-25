from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Reminder, Profile
import re

# ================= HOME =================
def home(request):
    return render(request, 'home.html')


# ================= REGISTER =================
def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        context = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email
        }

        # EMAIL FORMAT CHECK
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not email or not re.match(email_pattern, email):
            context['email_error'] = "Please enter a valid email address."
            return render(request, 'register.html', context)

        # PASSWORD MATCH & LENGTH
        if len(password) < 6:
            context['password_error'] = "Password must be at least 6 characters long."
            return render(request, 'register.html', context)

        if password != confirm_password:
            context['password_error'] = "Passwords do not match."
            return render(request, 'register.html', context)

        # DUPLICATE USER CHECK
        if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
            context['email_error'] = "An account with this email already exists. Please login."
            return render(request, 'register.html', context)

        # CREATE USER & PROFILE
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        Profile.objects.get_or_create(user=user)

        # AUTO LOGIN
        login(request, user)
        return redirect('dashboard')

    return render(request, 'register.html')


# ================= LOGIN =================
def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "login.html", {
                "error": "Invalid email or password. Please try again.",
                "email": email
            })

    return render(request, "login.html")


# ================= LOGOUT =================
def user_logout(request):
    logout(request)
    return redirect('login')


# ================= DASHBOARD =================
@login_required(login_url='login')
def dashboard(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    reminders = Reminder.objects.filter(user=request.user).order_by('date', 'time')

    total_count = reminders.count()
    taken_count = reminders.filter(status=True).count()
    pending_count = reminders.filter(status=False).count()

    context = {
        'profile': profile,
        'reminders': reminders,
        'total_count': total_count,
        'taken_count': taken_count,
        'pending_count': pending_count,
    }
    return render(request, 'dashboard.html', context)


# ================= ADD REMINDER =================
@login_required(login_url='login')
def add_reminder(request):
    if request.method == "POST":
        medicine = request.POST.get('medicine', '').strip()
        date = request.POST.get('date')
        time = request.POST.get('time')
        note = request.POST.get('note', '').strip()

        if medicine and date and time:
            Reminder.objects.create(
                user=request.user,
                medicine=medicine,
                date=date,
                time=time,
                note=note
            )
            return redirect('dashboard')
        else:
            return render(request, 'add_reminder.html', {
                'error': 'Please fill all required fields (Medicine Name, Date, Time).'
            })

    return render(request, 'add_reminder.html')


# ================= DELETE REMINDER =================
@login_required(login_url='login')
def delete_reminder(request, id):
    Reminder.objects.filter(id=id, user=request.user).delete()
    return redirect('dashboard')


# ================= TOGGLE / MARK TAKEN =================
@login_required(login_url='login')
def mark_taken(request, id):
    try:
        r = Reminder.objects.get(id=id, user=request.user)
        r.status = not r.status  # Toggles between Taken and Pending
        r.save()
    except Reminder.DoesNotExist:
        pass
    return redirect('dashboard')


# ================= EDIT REMINDER =================
@login_required(login_url='login')
def edit_reminder(request, id):
    reminder = get_object_or_404(Reminder, id=id, user=request.user)

    if request.method == "POST":
        reminder.medicine = request.POST.get('medicine', reminder.medicine).strip()
        new_date = request.POST.get('date')
        new_time = request.POST.get('time')
        if new_date:
            reminder.date = new_date
        if new_time:
            reminder.time = new_time
        reminder.note = request.POST.get('note', reminder.note).strip()
        reminder.save()
        return redirect('dashboard')

    return render(request, 'add_reminder.html', {
        'edit_reminder': reminder,
        'is_edit': True
    })


# ================= PROFILE VIEW =================
@login_required(login_url='login')
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        note = request.POST.get('note', '').strip()

        if first_name:
            request.user.first_name = first_name
        if last_name:
            request.user.last_name = last_name
        request.user.save()

        profile.note = note
        if request.FILES.get('photo'):
            profile.photo = request.FILES.get('photo')

        profile.save()
        return redirect('profile')

    return render(request, 'profile.html', {'profile': profile})


# ================= REST APIS =================

@api_view(['POST'])
def api_register(request):
    first_name = request.data.get('first_name', '')
    last_name = request.data.get('last_name', '')
    username = request.data.get('username', '').lower()
    password = request.data.get('password', '')

    if not username or not password:
        return Response({'status': 'error', 'message': 'Username and password required'}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({'status': 'error', 'message': 'User already exists'}, status=400)

    user = User.objects.create_user(
        username=username,
        email=username,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    Profile.objects.get_or_create(user=user)
    return Response({'status': 'registered', 'user_id': user.id})


@api_view(['POST'])
def api_login(request):
    username = request.data.get('username', '').lower()
    password = request.data.get('password', '')

    user = authenticate(username=username, password=password)
    if user is not None:
        return Response({'status': 'success', 'user_id': user.id, 'name': user.first_name})
    return Response({'status': 'failed', 'message': 'Invalid credentials'}, status=401)


@api_view(['POST'])
def api_logout(request):
    logout(request)
    return Response({'status': 'logged out'})


@api_view(['POST'])
def api_reset_password(request):
    username = request.data.get('username', '')
    new_password = request.data.get('new_password', '')

    try:
        user = User.objects.get(username=username)
        user.set_password(new_password)
        user.save()
        return Response({'status': 'password updated'})
    except User.DoesNotExist:
        return Response({'status': 'user not found'}, status=404)


@api_view(['POST'])
def api_add_reminder(request):
    if not request.user.is_authenticated:
        return Response({'status': 'unauthorized'}, status=401)

    medicine = request.data.get('medicine')
    date = request.data.get('date')
    time = request.data.get('time')
    note = request.data.get('note', '')

    r = Reminder.objects.create(
        user=request.user,
        medicine=medicine,
        date=date,
        time=time,
        note=note
    )
    return Response({'status': 'added', 'id': r.id})


@api_view(['GET'])
def api_reminders(request):
    if not request.user.is_authenticated:
        return Response({'status': 'unauthorized'}, status=401)

    data = list(Reminder.objects.filter(user=request.user).values())
    return Response(data)


@api_view(['POST', 'DELETE'])
def api_delete(request, id):
    if not request.user.is_authenticated:
        return Response({'status': 'unauthorized'}, status=401)

    deleted_count, _ = Reminder.objects.filter(id=id, user=request.user).delete()
    if deleted_count:
        return Response({'status': 'deleted'})
    return Response({'status': 'not found'}, status=404)


@api_view(['POST'])
def api_taken(request, id):
    if not request.user.is_authenticated:
        return Response({'status': 'unauthorized'}, status=401)

    try:
        r = Reminder.objects.get(id=id, user=request.user)
        r.status = not r.status
        r.save()
        return Response({'status': 'updated', 'taken': r.status})
    except Reminder.DoesNotExist:
        return Response({'status': 'not found'}, status=404)


@api_view(['GET'])
def api_profile(request):
    if not request.user.is_authenticated:
        return Response({'status': 'unauthorized'}, status=401)

    p, _ = Profile.objects.get_or_create(user=request.user)
    return Response({
        'name': f"{request.user.first_name} {request.user.last_name}".strip(),
        'email': request.user.email,
        'note': p.note,
        'photo': p.photo.url if p.photo else None
    })


@api_view(['POST'])
def api_profile_update(request):
    if not request.user.is_authenticated:
        return Response({'status': 'unauthorized'}, status=401)

    p, _ = Profile.objects.get_or_create(user=request.user)
    p.note = request.data.get('note', p.note)
    p.save()
    return Response({'status': 'updated'})
