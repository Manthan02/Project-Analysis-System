from django.db import models

# Create your models here.
class User(models.Model):
    user_id=models.AutoField(primary_key=True)
    username=models.TextField()
    email=models.EmailField()
    password=models.TextField()

class Project(models.Model):
    project_id=models.AutoField(primary_key=True)
    project_name=models.CharField(max_length=50)
    project_gname=models.CharField(max_length=50,null=True)
    project_group_id=models.IntegerField(null=True)
    project_admin=models.TextField()
    project_sdate=models.DateField(null=True)
    project_edate=models.DateField(null=True)
    project_type=models.CharField(max_length=7)

class Task(models.Model):
    task_id=models.AutoField(primary_key=True)
    task_name=models.CharField(max_length=50)
    task_project_name=models.CharField(max_length=50)
    task_project_id=models.IntegerField(null=True)
    user_name=models.TextField()
    task_status=models.IntegerField(null=True)
    task_sdate=models.DateField(null=True)
    task_edate=models.DateField(null=True)
    done_date=models.DateField(null=True)
    task_priority=models.IntegerField(null=True)

class Friend(models.Model):
    friend_of=models.TextField()
    friend_is=models.TextField()

class Friend_Request(models.Model):
    friend_request_id=models.AutoField(primary_key=True)
    friend_of=models.TextField()
    friend_is=models.TextField()

class Groups(models.Model):
    group_id=models.AutoField(primary_key=True)
    group_name=models.TextField()
    group_admin=models.TextField()

class Groups_Request(models.Model):
    group_request_id=models.AutoField(primary_key=True)
    group_id=models.IntegerField(null=True)
    group_admin=models.TextField()
    group_member=models.TextField()

class Groups_Members(models.Model):
    group_id=models.IntegerField(null=True)
    group_name=models.TextField()
    group_member=models.TextField()