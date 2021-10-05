from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
import random, string
from classroom.forms import CreateClassromForm
from django.contrib import messages

from classroom.models import ClassRoom

# Create your views here.

def codeGen(l=8):
    return ''.join(random.choice(string.ascii_uppercase+string.digits) for i in range(l))


@login_required(login_url='signin')
def createClassroom(request):
    if request.user.isTeacher:
        form = CreateClassromForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            classroom = form.save(commit=False)
            while(True):
                try:
                    classroom.code = codeGen()
                    classroom.user = request.user
                    classroom.save()
                    messages.add_message(request, messages.SUCCESS, "Classroom created successfully.")
                    return redirect('teacherDashboard')
                except:
                    pass
        context = {
            'form': form
        }
        return render(request, 'classroom/create.html', context)
    else:
        return redirect('studentDashboard')

    

@login_required(login_url='signin')
def classSearch(request):
    if request.user.isStudent:
        code = request.GET['code']
        context = {

        }
        try:
            classroom = get_object_or_404(ClassRoom,code=code)
            context.update({'classroom': classroom})
        except:
            messages.add_message(request, messages.ERROR, "No such classroom found.")
        return render(request, 'student/search-result.html', context)
    else:
        return redirect('teacherDashboard')