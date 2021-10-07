from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
import random, string
from classroom.forms import CreateClassromForm
from django.contrib import messages

from classroom.models import ClassRoom, Enroll

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

@login_required(login_url='sigin')
def classJoin(request,id):
    if request.user.isStudent:
        enroll = Enroll(user=request.user, classroom_id=id)
        try:
          enroll.save()
          messages.add_message(request, messages.SUCCESS, "You have joined this class successfully.")
        except:
          messages.add_message(request, messages.ERROR,"You have already joined this class.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
    else:
        return redirect('teacherDashboard')

@login_required(login_url='sigin')
def courseDetails(request,id):
    if request.user.isTeacher:
        context = {}
        try:
            classroom = ClassRoom.objects.get(id=id)
            enrolled_students = Enroll.objects.filter(classroom=classroom)
            context.update(
                {
                    'enrolled_students': enrolled_students,
                    'classroom': classroom
                })
        except Exception as e:
            messages.add_message(request, messages.ERROR, str(e))
        return render(request, 'teacher/course-details.html', context)
    else:
        return redirect('studentDashboard')


@login_required(login_url='signin')
def classroomJoinRequest(request, id):
    if request.user.isTeacher:
        try:
          enroll = Enroll.objects.get(id=id)
          enroll.status = True
          enroll.save()
          messages.add_message(request, messages.SUCCESS, "Classroom join request accepted successfully.")
        except:
            messages.add_message(request, messages.ERROR, str(e))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
    else:
        return redirect('studentDashboard')