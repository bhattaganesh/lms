from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
import random, string
from classroom.forms import CreateClassromForm
from django.contrib import messages

from classroom.models import ClassRoom, Enroll
from assignment.models import Comment, Post
from assignment.forms import CommentForm, PostForm

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
            try:
              enroll = Enroll.objects.get(classroom=classroom,user=request.user)
              if enroll.status:
                  context.update({'join': 'Joined'})
              else:
                  context.update({'join': 'Requested'})
            except:
                context.update({'join': 'Join'})
        except:
            messages.add_message(request, messages.ERROR, "No such classroom found.")
        context.update({'classroom': classroom})
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
        form = PostForm(request.POST or None, request.FILES or None)
        comment_form = CommentForm()
        comments = Comment.objects.all()
        posts = Post.objects.filter(classroom_id=id)
        if form.is_valid():
            form = form.save(commit=False)
            form.classroom_id = id
            form.user_id = request.user.id 
            form.save()
            messages.add_message(request, messages.SUCCESS, "Posted successfully.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 

        context = {}
        context.update({'form': form})
        context.update({'comment_form': comment_form})
        context.update({'posts': posts})
        context.update({'comments': comments})
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

@login_required(login_url='signin')
def postEdit(request, id):
    if request.user.isTeacher:
        post = get_object_or_404(Post,id=id)
        form = PostForm(request.POST or None, request.FILES or None , instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post Updated successfully.")
            return redirect("courseDetails", post.classroom.id)
        context = {
            'form': form
        }
        return render(request, 'teacher/post-edit.html', context)

@login_required(login_url='signin')
def postDelete(request, id):
    if request.user.isTeacher:
        post = get_object_or_404(Post,id=id)
        post.delete()
        messages.success(request, 'Post deleted successfully.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='signin')
def postComment(request, id):
    commentForm = CommentForm(request.POST)
    if commentForm.is_valid():
        comment = commentForm.save(commit=False)
        comment.post_id = id
        comment.user = request.user
        comment.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect('teacherDashboard')

