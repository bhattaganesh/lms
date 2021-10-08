from django.db import models
from classroom.models import ClassRoom
from myUser.models import User
from ckeditor.fields import RichTextField

# Create your models here.
class Assignment(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateField()
    marks = models.IntegerField(default=100)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    


class Submit(models.Model):
    obtainedMarks = models.IntegerField()
    submittedAt = models.DateField(auto_now=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.student.fullName

    class Meta:
        unique_together = ('assignment', 'student')


class  Post(models.Model):
    description = RichTextField(blank=True, null=True)
    # description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='post-files/', blank=True, null=True)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.description
