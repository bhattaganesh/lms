from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
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
        return render(request,'student/dashboard.html')
    return redirect('signin')
    # return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='signin')
def teacherDashboard(request):
    if request.user.isTeacher:
        return render(request,'teacher/dashboard.html')
    return redirect('signin')
    # return redirect(request.META.get('HTTP_REFERER'))



def signout(request):
    logout(request)
    return redirect('signin')