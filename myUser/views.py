from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from classroom.models import ClassRoom, Enroll
from myUser.forms import UserRegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def signin(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            if user.isStudent:
                return redirect('studentDashboard')
            elif user.isTeacher:
                return redirect('teacherDashboard')
            logout(request)
            messages.add_message(request, messages.ERROR, "Please, login with either student or teacher.")
            return redirect('signin')
        messages.add_message(request, messages.ERROR, "Sorry!, email or password does not match.")
    context = {
        'form': form
    }
    return render(request, 'signin.html', context)

def signupTeacher(request):
    form = UserRegistrationForm(request.POST or None)
    print(request.POST)
    if form.is_valid():
        user = form.save()
        user.isStudent = False
        user.isTeacher = True
        user.set_password(request.POST['password'])
        user.save()
        messages.add_message(request,messages.SUCCESS,'Registration Successful.')
        return redirect('signin')
    context = {
        'form': form
    }
    return render(request, 'teacher/signup.html',context)


def signupStudent(request):
    form = UserRegistrationForm(request.POST or None)
    print(request.POST)
    if form.is_valid():
        user = form.save()
        user.isStudent = True
        user.isTeacher = False
        user.set_password(request.POST['password'])
        user.save()
        messages.add_message(request,messages.SUCCESS,'Registration Successful.')
        return redirect('signin')
    context = {
        'form': form
    }
    return render(request, 'student/signup.html',context)

@login_required(login_url='signin')
def studentDashboard(request):
    if request.user.isStudent:
        classroom_ids = Enroll.objects.filter(user=request.user, status=True).values_list('classroom_id', flat=True)
        classrooms = ClassRoom.objects.filter(id__in=classroom_ids)
        return render(request,'student/dashboard.html', {'classrooms': classrooms})
    return redirect('teacherDashboard')

@login_required(login_url='signin')
def teacherDashboard(request):
    if request.user.isTeacher:
        classrooms = ClassRoom.objects.filter(user_id=request.user.id)
        context = {
            'classrooms': classrooms
        }
        return render(request,'teacher/dashboard.html', context)
    return redirect('studentDashboard')


def signout(request):
    logout(request)
    return redirect('signin')