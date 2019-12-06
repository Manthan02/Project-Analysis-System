from django.shortcuts import render,redirect
from .models import Project,Task,Friend,Groups,Friend_Request,Groups_Members,Groups_Request
from django.contrib.auth.models import User
from django.contrib.auth import login as lgin,logout as lgout
from datetime import timedelta,date 
# Create your views here.
def index(request):
        if request.user.is_authenticated:
                return redirect('main')
        return redirect('login')

def register(request):
        if request.method=='POST':
                username= request.POST['uname']
                email= request.POST['email']
                psw = request.POST['psw']
                if User.objects.filter(username=username).exists():
                        return render(request,'register.html')
                if User.objects.filter(email=email).exists():
                        return render(request,'register.html')
                else:   
                        if request.POST['rpsw'] == psw: 
                                user=User.objects.create()
                                user.username=username
                                user.email=email
                                user.password=psw
                                user.save()
                                return redirect('login')
        return render(request,'register.html')

def main(request):
        fr=Friend_Request.objects.filter(friend_is=request.user).count()
        gr=Groups_Request.objects.filter(group_member=request.user).count()
        tot=fr+gr
        return render(request,'main.html',context={
                "PC":Project.objects.filter(project_admin=request.user).count(),
                "TC":Task.objects.filter(user_name=request.user).count(),
                "GC":Groups_Members.objects.filter(group_member=request.user).count(),
                "FC":Friend.objects.filter(friend_of=request.user).count(),
                "FR":tot})

def login(request):
        if request.method=='POST':
                email= request.POST['email']
                psw = request.POST['psw']
                if User.objects.filter(email=email,password=psw).exists():
                        user=User.objects.get(email=email,password=psw)
                        lgin(request,user)
                        return redirect('main')
                else:   
                        return render(request, 'home.html')
        return render(request, 'home.html') 

def logout(request):
        lgout(request)
        return redirect('login')

def projects(request):
        user=request.user
        fr=Friend_Request.objects.filter(friend_is=request.user).count()
        gr=Groups_Request.objects.filter(group_member=request.user).count()
        tot=fr+gr
        return render(request,'projects.html',context={
                "Project":Project.objects.filter(project_admin=user),
                "PC":Project.objects.filter(project_admin=request.user).count(),
                "TC":Task.objects.filter(user_name=request.user).count(),
                "GC":Groups_Members.objects.filter(group_member=request.user).count(),
                "FC":Friend.objects.filter(friend_of=request.user).count(),
                "FR":tot})

def groupshow(request,group_id):
        fr=Friend_Request.objects.filter(friend_is=request.user).count()
        gr=Groups_Request.objects.filter(group_member=request.user).count()
        tot=fr+gr
        request.session['grpid']=group_id
        return render(request,'groupshow.html',context={
                "PC":Project.objects.filter(project_admin=request.user).count(),
                "TC":Task.objects.filter(user_name=request.user).count(),
                "GC":Groups_Members.objects.filter(group_member=request.user).count(),
                "FC":Friend.objects.filter(friend_of=request.user).count(),
                "Group":Groups.objects.filter(group_id=group_id),
                "GM":Groups_Members.objects.filter(group_id=group_id),
                "FR":tot})

def projectshow(request,project_id):
        user=request.user
        all_to_do=Task.objects.filter(task_project_id=project_id,task_status=1)
        user_to_do=all_to_do.filter(user_name=user)
        other_to_do=all_to_do.exclude(user_name=user)
        all_in_pro=Task.objects.filter(task_project_id=project_id,task_status=2)
        user_in_pro=all_in_pro.filter(user_name=user)
        other_in_pro=all_in_pro.exclude(user_name=user)
        all_done=Task.objects.filter(task_project_id=project_id,task_status=3)
        user_done=all_done.filter(user_name=user)
        other_done=all_done.exclude(user_name=user)
        fr=Friend_Request.objects.filter(friend_is=request.user).count()
        gr=Groups_Request.objects.filter(group_member=request.user).count()
        tot=fr+gr
        return render(request,'projectview.html',context={
                "Project":Project.objects.filter(project_id=project_id),
                "user_to_do":user_to_do,
                "other_to_do":other_to_do,
                "user_in_pro":user_in_pro,
                "other_in_pro":other_in_pro,
                "user_done":user_done,
                "other_done":other_done,
                "u1":user,
                "FR":tot
                })

def to_do(request,project_id,task_id):
        user=request.user
        task=Task.objects.get(task_id=task_id,task_project_id=project_id)
        task.task_status=1
        task.done_date=None
        task.save()
        all_to_do=Task.objects.filter(task_project_id=project_id,task_status=1)
        user_to_do=all_to_do.filter(user_name=user)
        other_to_do=all_to_do.exclude(user_name=user)
        all_in_pro=Task.objects.filter(task_project_id=project_id,task_status=2)
        user_in_pro=all_in_pro.filter(user_name=user)
        other_in_pro=all_in_pro.exclude(user_name=user)
        all_done=Task.objects.filter(task_project_id=project_id,task_status=3)
        user_done=all_done.filter(user_name=user)
        other_done=all_done.exclude(user_name=user)
        fr=Friend_Request.objects.filter(friend_is=request.user).count()
        gr=Groups_Request.objects.filter(group_member=request.user).count()
        tot=fr+gr
        return render(request,'projectview.html',context={
                "Project":Project.objects.filter(project_id=project_id),
                "user_to_do":user_to_do,
                "other_to_do":other_to_do,
                "user_in_pro":user_in_pro,
                "other_in_pro":other_in_pro,
                "user_done":user_done,
                "other_done":other_done,
                "u1":user,
                "FR":tot
                })

def in_pro(request,project_id,task_id):
        user=request.user
        task=Task.objects.get(task_id=task_id,task_project_id=project_id)
        task.task_status=2
        task.done_date=None
        task.save()
        all_to_do=Task.objects.filter(task_project_id=project_id,task_status=1)
        user_to_do=all_to_do.filter(user_name=user)
        other_to_do=all_to_do.exclude(user_name=user)
        all_in_pro=Task.objects.filter(task_project_id=project_id,task_status=2)
        user_in_pro=all_in_pro.filter(user_name=user)
        other_in_pro=all_in_pro.exclude(user_name=user)
        all_done=Task.objects.filter(task_project_id=project_id,task_status=3)
        user_done=all_done.filter(user_name=user)
        other_done=all_done.exclude(user_name=user)
        fr=Friend_Request.objects.filter(friend_is=request.user).count()
        gr=Groups_Request.objects.filter(group_member=request.user).count()
        tot=fr+gr
        return render(request,'projectview.html',context={
                "Project":Project.objects.filter(project_id=project_id),
                "user_to_do":user_to_do,
                "other_to_do":other_to_do,
                "user_in_pro":user_in_pro,
                "other_in_pro":other_in_pro,
                "user_done":user_done,
                "other_done":other_done,
                "u1":user,
                "FR":tot
                })

def done(request,project_id,task_id):
        user=request.user
        task=Task.objects.get(task_id=task_id,task_project_id=project_id)
        task.task_status=3
        task.done_date=date.today()
        task.save()
        all_to_do=Task.objects.filter(task_project_id=project_id,task_status=1)
        user_to_do=all_to_do.filter(user_name=user)
        other_to_do=all_to_do.exclude(user_name=user)
        all_in_pro=Task.objects.filter(task_project_id=project_id,task_status=2)
        user_in_pro=all_in_pro.filter(user_name=user)
        other_in_pro=all_in_pro.exclude(user_name=user)
        all_done=Task.objects.filter(task_project_id=project_id,task_status=3)
        user_done=all_done.filter(user_name=user)
        other_done=all_done.exclude(user_name=user)
        fr=Friend_Request.objects.filter(friend_is=request.user).count()
        gr=Groups_Request.objects.filter(group_member=request.user).count()
        tot=fr+gr
        return render(request,'projectview.html',context={
                "Project":Project.objects.filter(project_id=project_id),
                "user_to_do":user_to_do,
                "other_to_do":other_to_do,
                "user_in_pro":user_in_pro,
                "other_in_pro":other_in_pro,
                "user_done":user_done,
                "other_done":other_done,
                "u1":user,
                "FR":tot
                })



def tasks(request):
        user=request.user
        fr=Friend_Request.objects.filter(friend_is=request.user).count()
        gr=Groups_Request.objects.filter(group_member=request.user).count()
        tot=fr+gr
        return render(request,'tasks.html',context={
                "Task":Task.objects.filter(user_name=user),
                "PC":Project.objects.filter(project_admin=request.user).count(),
                "TC":Task.objects.filter(user_name=request.user).count(),
                "GC":Groups_Members.objects.filter(group_member=request.user).count(),
                "FC":Friend.objects.filter(friend_of=request.user).count(),
                "Project":Project.objects.filter(project_type='Public'),
                "Friend":Friend.objects.filter(friend_is=user),
                "FR":tot})
def backlog(request,project_id):
        user=request.user
        p1=Project.objects.get(project_id=project_id)
        fr=Friend_Request.objects.filter(friend_is=request.user).count()
        gr=Groups_Request.objects.filter(group_member=request.user).count()
        tot=fr+gr
        grp_id=Groups.objects.get(group_admin=user.username,group_id=p1.project_group_id)
        if p1.project_admin == user.username :
                if request.method=='POST':
                        taskname=request.POST['tname']
                        prio=request.POST['prio']
                        task=Task.objects.create()
                        task.task_name=taskname
                        task.task_project_name=p1.project_name
                        task.task_project_id=project_id
                        task.task_priority=prio
                        task.task_status=0
                        task.save()
                        return render(request,'backlog.html',context={
                        "Project":Project.objects.filter(project_admin=user),
                        "PC":Project.objects.filter(project_admin=request.user).count(),
                        "TC":Task.objects.filter(user_name=request.user).count(),
                        "GC":Groups_Members.objects.filter(group_member=request.user).count(),
                        "FC":Friend.objects.filter(friend_of=request.user).count(),
                        "Group":Groups_Members.objects.filter(group_id=grp_id.group_id),
                        "Task":Task.objects.filter(task_project_id=project_id,task_status=0),
                        "high":Task.objects.filter(task_project_id=project_id,task_status=0,task_priority=1),
                        "common":Task.objects.filter(task_project_id=project_id,task_status=0,task_priority=2),
                        "low":Task.objects.filter(task_project_id=project_id,task_status=0,task_priority=3),
                        "FR":tot})
                return render(request,'backlog.html',context={
                        "Project":Project.objects.filter(project_admin=user),
                        "PC":Project.objects.filter(project_admin=request.user).count(),
                        "TC":Task.objects.filter(user_name=request.user).count(),
                        "GC":Groups_Members.objects.filter(group_member=request.user).count(),
                        "FC":Friend.objects.filter(friend_of=request.user).count(),
                        "Group":Groups_Members.objects.filter(group_id=grp_id.group_id),
                        "Task":Task.objects.filter(task_project_id=project_id,task_status=0),
                        "high":Task.objects.filter(task_project_id=project_id,task_status=0,task_priority=1),
                        "common":Task.objects.filter(task_project_id=project_id,task_status=0,task_priority=2),
                        "low":Task.objects.filter(task_project_id=project_id,task_status=0,task_priority=3),
                        "FR":tot})
        else:
                all_to_do=Task.objects.filter(task_project_id=project_id,task_status=1)
                user_to_do=all_to_do.filter(user_name=user)
                other_to_do=all_to_do.exclude(user_name=user)
                all_in_pro=Task.objects.filter(task_project_id=project_id,task_status=2)
                user_in_pro=all_in_pro.filter(user_name=user)
                other_in_pro=all_in_pro.exclude(user_name=user)
                all_done=Task.objects.filter(task_project_id=project_id,task_status=3)
                user_done=all_done.filter(user_name=user)
                other_done=all_done.exclude(user_name=user)

                return render(request,'projectview.html',context={
                        "Project":Project.objects.filter(project_id=project_id),
                        "user_to_do":user_to_do,
                        "other_to_do":other_to_do,
                        "user_in_pro":user_in_pro,
                        "other_in_pro":other_in_pro,
                        "user_done":user_done,
                        "other_done":other_done,
                        "u1":user,
                        "FR":tot
                        })

def addtask(request,project_id):
        user=request.user
        p1=Project.objects.get(project_id=project_id)
        fr=Friend_Request.objects.filter(friend_is=request.user).count()
        gr=Groups_Request.objects.filter(group_member=request.user).count()
        tot=fr+gr
        grp_id=Groups.objects.get(group_admin=user.username,group_id=p1.project_group_id)
        if p1.project_admin == user.username :
                if request.method=='POST':
                        taskname=request.POST['tname']
                        member=request.POST['mname']
                        task=Task.objects.get(task_id=taskname)
                        task.user_name=member
                        task.task_status=1
                        task.save()
                        all_to_do=Task.objects.filter(task_project_id=project_id,task_status=1)
                        user_to_do=all_to_do.filter(user_name=user)
                        other_to_do=all_to_do.exclude(user_name=user)
                        all_in_pro=Task.objects.filter(task_project_id=project_id,task_status=2)
                        user_in_pro=all_in_pro.filter(user_name=user)
                        other_in_pro=all_in_pro.exclude(user_name=user)
                        all_done=Task.objects.filter(task_project_id=project_id,task_status=3)
                        user_done=all_done.filter(user_name=user)
                        other_done=all_done.exclude(user_name=user)

                        return render(request,'projectview.html',context={
                                "Project":Project.objects.filter(project_id=project_id),
                                "user_to_do":user_to_do,
                                "other_to_do":other_to_do,
                                "user_in_pro":user_in_pro,
                                "other_in_pro":other_in_pro,
                                "user_done":user_done,
                                "other_done":other_done,
                                "u1":user,
                                "FR":tot
                                }) 
                        # return render(request,'addtask.html',context={
                        #         "Project":Project.objects.filter(project_admin=user),
                        #         "PC":Project.objects.filter(project_admin=request.user).count(),
                        #         "TC":Task.objects.filter(user_name=request.user).count(),
                        #         "GC":Groups_Members.objects.filter(group_member=request.user).count(),
                        #         "FC":Friend.objects.filter(friend_of=request.user).count(),
                        #         "Group":Groups_Members.objects.filter(group_id=grp_id),
                        #         "Task":Task.objects.filter(task_project_id=project_id),
                        #         "FR":tot})
                return render(request,'addtask.html',context={
                        "Project":Project.objects.filter(project_admin=user),
                        "PC":Project.objects.filter(project_admin=request.user).count(),
                        "TC":Task.objects.filter(user_name=request.user).count(),
                        "GC":Groups_Members.objects.filter(group_member=request.user).count(),
                        "FC":Friend.objects.filter(friend_of=request.user).count(),
                        "Group":Groups_Members.objects.filter(group_id=grp_id.group_id),
                        "Task":Task.objects.filter(task_project_id=project_id),
                        "backlog":Task.objects.filter(task_project_id=project_id,task_status=0),
                        "high":Task.objects.filter(task_project_id=project_id,task_status=0,task_priority=1),
                        "common":Task.objects.filter(task_project_id=project_id,task_status=0,task_priority=2),
                        "low":Task.objects.filter(task_project_id=project_id,task_status=0,task_priority=3),
                        "FR":tot})
        else:
                all_to_do=Task.objects.filter(task_project_id=project_id,task_status=1)
                user_to_do=all_to_do.filter(user_name=user)
                other_to_do=all_to_do.exclude(user_name=user)
                all_in_pro=Task.objects.filter(task_project_id=project_id,task_status=2)
                user_in_pro=all_in_pro.filter(user_name=user)
                other_in_pro=all_in_pro.exclude(user_name=user)
                all_done=Task.objects.filter(task_project_id=project_id,task_status=3)
                user_done=all_done.filter(user_name=user)
                other_done=all_done.exclude(user_name=user)

                return render(request,'projectview.html',context={
                        "Project":Project.objects.filter(project_id=project_id),
                        "user_to_do":user_to_do,
                        "other_to_do":other_to_do,
                        "user_in_pro":user_in_pro,
                        "other_in_pro":other_in_pro,
                        "user_done":user_done,
                        "other_done":other_done,
                        "u1":user,
                        "FR":tot
                        })     

def chart(request,project_id):
        fr=Friend_Request.objects.filter(friend_is=request.user).count()
        gr=Groups_Request.objects.filter(group_member=request.user).count()
        totr=fr+gr
        tado=Task.objects.filter(task_project_id=project_id,task_status=1).count()
        in_pro=Task.objects.filter(task_project_id=project_id,task_status=2).count()
        done=Task.objects.filter(task_project_id=project_id,task_status=3).count()
        tot=tado+in_pro+done
        tp=(tado/tot)*100
        ip=(in_pro/tot)*100
        dp=(done/tot)*100
        project=Project.objects.get(project_id=project_id)
        group=Groups_Members.objects.filter(group_id=project.project_group_id)
        task=Task.objects.filter(task_project_id=project_id)
        if request.method=='POST':
                member=request.POST['tname']
                mtdc=Task.objects.filter(user_name=member,task_status=1,task_project_id=project_id).count()
                mipc=Task.objects.filter(user_name=member,task_status=2,task_project_id=project_id).count()
                mdoc=Task.objects.filter(user_name=member,task_status=3,task_project_id=project_id).count()
                mtot=mtdc+mdoc+mipc
                mtp=(mtdc/mtot)*100
                mip=(mipc/mtot)*100
                mdp=(mdoc/mtot)*100
                return render(request,'chart.html',context={
                "PC":Project.objects.filter(project_admin=request.user).count(),
                "TC":Task.objects.filter(user_name=request.user).count(),
                "GC":Groups_Members.objects.filter(group_member=request.user).count(),
                "FC":Friend.objects.filter(friend_of=request.user).count(),
                "pro":Project.objects.filter(project_id=project_id),
                "user":member,
                "group":group,
                "task":Task.objects.filter(task_project_id=project_id),
                "to_do":tp,
                "in_pro":ip,
                "done":dp,
                "mtdc":mtp,
                "mipc":mip,
                "mdoc":mdp,
                "members":Groups_Members.objects.filter(group_id=project.project_group_id),
                "FR":totr})
          
        else :
                return render(request,'chart.html',context={
                        "PC":Project.objects.filter(project_admin=request.user).count(),
                        "TC":Task.objects.filter(user_name=request.user).count(),
                        "GC":Groups_Members.objects.filter(group_member=request.user).count(),
                        "FC":Friend.objects.filter(friend_of=request.user).count(),
                        "pro":Project.objects.filter(project_id=project_id),
                        "group":group,
                        "task":Task.objects.filter(task_project_id=project_id),
                        "to_do":tp,
                        "in_pro":ip,
                        "done":dp,
                        "members":Groups_Members.objects.filter(group_id=project.project_group_id),
                        "FR":totr})

def burndown(request,project_id):
        project=Project.objects.get(project_id=project_id)
        sdate=project.project_sdate
        ldate=project.project_edate
        delta=ldate-sdate
        total_task=Task.objects.filter(task_project_id=project_id).count()
        total_task1=Task.objects.filter(task_project_id=project_id).count()
        year={}
        month={}
        day={}
        task={}
        count={}
        comp_task={}
        # print(sdate)
        # print(sdate+timedelta(days=7))
        if delta.days <= 84 :
                burntask=total_task/(delta.days/7)
                tmp_sdate=sdate-timedelta(days=7)
                total_task=total_task+burntask
                count_date=sdate
                complete_task=0
                totl_day=0
                while count_date <=date.today():
                        temp_task_count=Task.objects.filter(task_status=3,done_date=count_date).count()
                        complete_task=complete_task+temp_task_count
                        count_date=count_date+timedelta(days=1)
                        totl_day=totl_day+1
                taskspeed=complete_task/totl_day
                k=0
                
                while k<12:
                        week_task=0
                        pre_sdate=tmp_sdate
                        tmp_sdate=tmp_sdate+timedelta(days=7)
                        while pre_sdate <= tmp_sdate:
                                if pre_sdate <= date.today():
                                        temp_task_count=Task.objects.filter(task_status=3,done_date=pre_sdate).count()
                                        week_task=week_task+temp_task_count
                                        pre_sdate=pre_sdate+timedelta(days=1)
                                else:
                                        week_task=week_task+taskspeed
                                        pre_sdate=pre_sdate+timedelta(days=1)
                        count[k]=week_task
                        k=k+1

                k=0       
                while k<12:
                        if total_task-count[k] >= 0:
                                comp_task[k]=total_task-count[k]
                                total_task=total_task-count[k]
                        else:
                                comp_task[k]=0
                        k=k+1
                tmp_sdate=sdate-timedelta(days=7)
                k=0
                total_task1=total_task1+burntask
                while k<12:
                        tmp_sdate=tmp_sdate+timedelta(days=7)
                        year[k]=tmp_sdate.year 
                        month[k]=tmp_sdate.month
                        day[k]=tmp_sdate.day
                        total_task1=total_task1-burntask
                        if total_task1 > 0:
                                task[k]=total_task1
                        else:
                                task[k]=0
                        k+=1
                return render(request,'burndown.html',context={
                "burntask":burntask,
                "y0":year[0],"m0":month[0],"d0":day[0],"t0":task[0],"ct0":comp_task[0],
                "y1":year[1],"m1":month[1],"d1":day[1],"t1":task[1],"ct1":comp_task[1],
                "y2":year[2],"m2":month[2],"d2":day[2],"t2":task[2],"ct2":comp_task[2],
                "y3":year[3],"m3":month[3],"d3":day[3],"t3":task[3],"ct3":comp_task[3],
                "y4":year[4],"m4":month[4],"d4":day[4],"t4":task[4],"ct4":comp_task[4],
                "y5":year[5],"m5":month[5],"d5":day[5],"t5":task[5],"ct5":comp_task[5],
                "y6":year[6],"m6":month[6],"d6":day[6],"t6":task[6],"ct6":comp_task[6],
                "y7":year[7],"m7":month[7],"d7":day[7],"t7":task[7],"ct7":comp_task[7],
                "y8":year[8],"m8":month[8],"d8":day[8],"t8":task[8],"ct8":comp_task[8],
                "y9":year[9],"m9":month[9],"d9":day[9],"t9":task[9],"ct9":comp_task[9],
                "y10":year[10],"m10":month[10],"d10":day[10],"t10":task[10],"ct10":comp_task[10],
                "y11":year[11],"m11":month[11],"d11":day[11],"t11":task[11],"ct11":comp_task[11],
                })
        elif delta.days <= 365 :
                burntask=total_task/(delta.days/30)
                tmp_sdate=sdate-timedelta(days=30)
                total_task=total_task+burntask
                count_date=sdate
                complete_task=0
                totl_day=0
                while count_date <=date.today():
                        temp_task_count=Task.objects.filter(task_status=3,done_date=count_date).count()
                        complete_task=complete_task+temp_task_count
                        count_date=count_date+timedelta(days=1)
                        totl_day=totl_day+1
                taskspeed=complete_task/totl_day
                k=0
                
                while k<12:
                        week_task=0
                        pre_sdate=tmp_sdate
                        tmp_sdate=tmp_sdate+timedelta(days=30)
                        while pre_sdate <= tmp_sdate:
                                if pre_sdate <= date.today():
                                        temp_task_count=Task.objects.filter(task_status=3,done_date=pre_sdate).count()
                                        week_task=week_task+temp_task_count
                                        pre_sdate=pre_sdate+timedelta(days=1)
                                else:
                                        week_task=week_task+taskspeed
                                        pre_sdate=pre_sdate+timedelta(days=1)
                        count[k]=week_task
                        k=k+1

                k=0        
                while k<12:
                        if total_task-count[k] >= 0:
                                comp_task[k]=total_task-count[k]
                                total_task=total_task-count[k]
                        else:
                                comp_task[k]=0
                        k=k+1
                tmp_sdate=sdate-timedelta(days=30)
                k=0
                while k<12:
                        tmp_sdate=tmp_sdate+timedelta(days=30)
                        year[k]=tmp_sdate.year 
                        month[k]=tmp_sdate.month
                        day[k]=tmp_sdate.day
                        total_task1=total_task1-burntask
                        if total_task1 >= 0:
                                task[k]=total_task1
                        else:
                                task[k]=0
                        k+=1
                return render(request,'burndown.html',context={
                "burntask":burntask,
                "y0":year[0],"m0":month[0],"d0":day[0],"t0":task[0],"ct0":comp_task[0],
                "y1":year[1],"m1":month[1],"d1":day[1],"t1":task[1],"ct1":comp_task[1],
                "y2":year[2],"m2":month[2],"d2":day[2],"t2":task[2],"ct2":comp_task[2],
                "y3":year[3],"m3":month[3],"d3":day[3],"t3":task[3],"ct3":comp_task[3],
                "y4":year[4],"m4":month[4],"d4":day[4],"t4":task[4],"ct4":comp_task[4],
                "y5":year[5],"m5":month[5],"d5":day[5],"t5":task[5],"ct5":comp_task[5],
                "y6":year[6],"m6":month[6],"d6":day[6],"t6":task[6],"ct6":comp_task[6],
                "y7":year[7],"m7":month[7],"d7":day[7],"t7":task[7],"ct7":comp_task[7],
                "y8":year[8],"m8":month[8],"d8":day[8],"t8":task[8],"ct8":comp_task[8],
                "y9":year[9],"m9":month[9],"d9":day[9],"t9":task[9],"ct9":comp_task[9],
                "y10":year[10],"m10":month[10],"d10":day[10],"t10":task[10],"ct10":comp_task[10],
                "y11":year[11],"m11":month[11],"d11":day[11],"t11":task[11],"ct11":comp_task[11],
                })
        return render(request,'burndown.html',context={
        "total_task":total_task,
        "burntask":burntask,
        "sdate":sdate        
        })

def groups(request):
        user=request.user
        fr=Friend_Request.objects.filter(friend_is=request.user).count()
        gr=Groups_Request.objects.filter(group_member=request.user).count()
        tot=fr+gr
        return render(request,'groups.html',context={
                "Group":Groups_Members.objects.filter(group_member=request.user),
                "PC":Project.objects.filter(project_admin=request.user).count(),
                "TC":Task.objects.filter(user_name=request.user).count(),
                "GC":Groups_Members.objects.filter(group_member=request.user).count(),
                "FC":Friend.objects.filter(friend_of=request.user).count(),
                "FR":tot})

def friends(request):
        user=request.user
        fr=Friend_Request.objects.filter(friend_is=request.user).count()
        gr=Groups_Request.objects.filter(group_member=request.user).count()
        tot=fr+gr
        return render(request,'friends.html',context={
                "Friend":Friend.objects.filter(friend_of=user),
                "PC":Project.objects.filter(project_admin=request.user).count(),
                "TC":Task.objects.filter(user_name=request.user).count(),
                "GC":Groups_Members.objects.filter(group_member=request.user).count(),
                "FC":Friend.objects.filter(friend_of=request.user).count(),
                "FR":tot})

def requests(request):
        user=request.user
        fr=Friend_Request.objects.filter(friend_is=request.user).count()
        gr=Groups_Request.objects.filter(group_member=request.user).count()
        tot=fr+gr
        return render(request,'requests.html',context={
                "Friend":Friend.objects.filter(friend_of=user),
                "PC":Project.objects.filter(project_admin=request.user).count(),
                "TC":Task.objects.filter(user_name=request.user).count(),
                "GC":Groups_Members.objects.filter(group_member=request.user).count(),
                "FC":Friend.objects.filter(friend_of=request.user).count(),
                "FR":tot,
                "requests":Friend_Request.objects.filter(friend_is=request.user),
                "grp_request":Groups_Request.objects.filter(group_member=request.user),
                })

def friend_accept(request,friend_request_id):        
        user=request.user
        fri_req=Friend_Request.objects.get(friend_request_id=friend_request_id)
        fri1=Friend.objects.create()
        fri1.friend_of=fri_req.friend_of
        fri1.friend_is=fri_req.friend_is
        fri1.save()
        fri2=Friend.objects.create()
        fri2.friend_of=fri_req.friend_is
        fri2.friend_is=fri_req.friend_of
        fri2.save()
        Friend_Request.objects.get(friend_request_id=friend_request_id).delete()
        fr=Friend_Request.objects.filter(friend_is=request.user).count()
        gr=Groups_Request.objects.filter(group_member=request.user).count()
        tot=fr+gr
        return render(request,'requests.html',context={
                "Friend":Friend.objects.filter(friend_of=user),
                "PC":Project.objects.filter(project_admin=request.user).count(),
                "TC":Task.objects.filter(user_name=request.user).count(),
                "GC":Groups_Members.objects.filter(group_member=request.user).count(),
                "FC":Friend.objects.filter(friend_of=request.user).count(),
                "FR":tot,
                "requests":Friend_Request.objects.filter(friend_is=request.user)
                })

def friend_decline(request,friend_request_id):        
        user=request.user
        Friend_Request.objects.get(friend_request_id=friend_request_id).delete()
        fr=Friend_Request.objects.filter(friend_is=request.user).count()
        gr=Groups_Request.objects.filter(group_member=request.user).count()
        tot=fr+gr
        return render(request,'requests.html',context={
                "Friend":Friend.objects.filter(friend_of=user),
                "PC":Project.objects.filter(project_admin=request.user).count(),
                "TC":Task.objects.filter(user_name=request.user).count(),
                "GC":Groups_Members.objects.filter(group_member=request.user).count(),
                "FC":Friend.objects.filter(friend_of=request.user).count(),
                "FR":tot,
                "requests":Friend_Request.objects.filter(friend_is=request.user)
                })

def group_accept(request,group_request_id):        
        user=request.user
        grp_req=Groups_Request.objects.get(group_request_id=group_request_id)
        grp=Groups.objects.get(group_id=grp_req.group_id)
        grp_mem=Groups_Members.objects.create()
        grp_mem.group_id=grp_req.group_id
        grp_mem.group_name=grp.group_name
        grp_mem.group_member=user.username
        grp_mem.save()
        Groups_Request.objects.get(group_request_id=group_request_id).delete()
        fr=Friend_Request.objects.filter(friend_is=request.user).count()
        gr=Groups_Request.objects.filter(group_member=request.user).count()
        tot=fr+gr
        return render(request,'requests.html',context={
                "Friend":Friend.objects.filter(friend_of=user),
                "PC":Project.objects.filter(project_admin=request.user).count(),
                "TC":Task.objects.filter(user_name=request.user).count(),
                "GC":Groups_Members.objects.filter(group_member=request.user).count(),
                "FC":Friend.objects.filter(friend_of=request.user).count(),
                "FR":tot,
                "requests":Friend_Request.objects.filter(friend_is=request.user)
                })

def group_decline(request,group_request_id):        
        user=request.user
        grp_req=Groups_Request.objects.get(group_request_id=group_request_id)
        grp=Groups.objects.get(group_id=grp_req.group_id)
        Groups_Request.objects.get(group_request_id=group_request_id).delete()
        fr=Friend_Request.objects.filter(friend_is=request.user).count()
        gr=Groups_Request.objects.filter(group_member=request.user).count()
        tot=fr+gr
        return render(request,'requests.html',context={
                "Friend":Friend.objects.filter(friend_of=user),
                "PC":Project.objects.filter(project_admin=request.user).count(),
                "TC":Task.objects.filter(user_name=request.user).count(),
                "GC":Groups_Members.objects.filter(group_member=request.user).count(),
                "FC":Friend.objects.filter(friend_of=request.user).count(),
                "FR":tot,
                "requests":Friend_Request.objects.filter(friend_is=request.user)
                })

def private_add(request):
        user=request.user
        fr=Friend_Request.objects.filter(friend_is=request.user).count()
        gr=Groups_Request.objects.filter(group_member=request.user).count()
        tot=fr+gr
        if request.method=='POST':
                projectname= request.POST['pname']
                groupid= request.POST['gname']
                sdate=request.POST['sdate']
                edate=request.POST['edate']
                pro=Project.objects.create()
                pro.project_name=projectname
                pro.project_admin=user.username
                pro.project_sdate=sdate
                pro.project_edate=edate
                pro.project_group_id=groupid
                grpname=Groups.objects.get(group_id=groupid)
                pro.project_gname=grpname.group_name
                pro.project_type="Private"
                pro.save()
                request.session['grpid']=pro.project_group_id
                request.session['proname']=pro.project_name
                request.session['proid']=pro.project_id
                return redirect('projects')

        return render(request,'private_add.html',context={
                "Project":Project.objects.filter(project_admin=user),
                "PC":Project.objects.filter(project_admin=request.user).count(),
                "TC":Task.objects.filter(user_name=request.user).count(),
                "GC":Groups_Members.objects.filter(group_member=request.user).count(),
                "FC":Friend.objects.filter(friend_of=request.user).count(),
                "Group":Groups.objects.filter(group_admin=request.user),
                "FR":tot})

def private_task_add(request):
        user=request.user
        proid=request.session['proid']
        proname=request.session['proname']
        grp_id=request.session['grpid']
        if request.method=='POST':
                taskname=request.POST['tname']
                member=request.POST['mname']
                task=Task.objects.create()
                task.task_name=taskname
                task.task_project_name=proname
                task.task_project_id=proid
                task.user_name=member
                task.task_status=1
                task.save()
                return redirect('private_task_add')
        fr=Friend_Request.objects.filter(friend_is=request.user).count()
        gr=Groups_Request.objects.filter(group_member=request.user).count()
        tot=fr+gr
        return render(request,'private_task_add.html',context={
                "Project":Project.objects.filter(project_admin=user),
                "PC":Project.objects.filter(project_admin=request.user).count(),
                "TC":Task.objects.filter(user_name=request.user).count(),
                "GC":Groups_Members.objects.filter(group_member=request.user).count(),
                "FC":Friend.objects.filter(friend_of=request.user).count(),
                "Group":Groups_Members.objects.filter(group_id=grp_id),
                "Task":Task.objects.filter(task_project_id=proid),
                "FR":tot})


def project_type(request):
        user=request.user
        fr=Friend_Request.objects.filter(friend_is=request.user).count()
        gr=Groups_Request.objects.filter(group_member=request.user).count()
        tot=fr+gr
        return render(request,'project_type.html',context={
                "Project":Project.objects.filter(project_admin=user),
                "PC":Project.objects.filter(project_admin=request.user).count(),
                "TC":Task.objects.filter(user_name=request.user).count(),
                "GC":Groups_Members.objects.filter(group_member=request.user).count(),
                "FC":Friend.objects.filter(friend_of=request.user).count(),
                "FR":tot})

def public_add(request):
        user=request.user
        fr=Friend_Request.objects.filter(friend_is=request.user).count()
        gr=Groups_Request.objects.filter(group_member=request.user).count()
        tot=fr+gr
        if request.method=='POST':
                projectname= request.POST['pname']
                
                sdate=request.POST['sdate']
                edate=request.POST['edate']
                pro=Project.objects.create()
                pro.project_name=projectname
                pro.project_admin=user.username
                pro.project_sdate=sdate
                pro.project_edate=edate
                
                pro.project_type="Public"
                pro.save()
                request.session['proname']=pro.project_name
                request.session['proid']=pro.project_id
                return redirect('public_task_add')
        return render(request,'public_add.html',context={
                "Project":Project.objects.filter(project_admin=user),
                "PC":Project.objects.filter(project_admin=request.user).count(),
                "TC":Task.objects.filter(user_name=request.user).count(),
                "GC":Groups_Members.objects.filter(group_member=request.user).count(),
                "FC":Friend.objects.filter(friend_of=request.user).count(),
                "FR":tot})

def public_task_add(request):
        user=request.user
        proid=request.session['proid']
        proname=request.session['proname']
        fr=Friend_Request.objects.filter(friend_is=request.user).count()
        gr=Groups_Request.objects.filter(group_member=request.user).count()
        tot=fr+gr
        if request.method=='POST':
                taskname=request.POST['tname']
                
                task=Task.objects.create()
                task.task_name=taskname
                task.task_project_name=proname
                task.task_project_id=proid
                
                task.save()
                return redirect('public_task_add')
        
        return render(request,'public_task_add.html',context={
                "Project":Project.objects.filter(project_admin=user),
                "PC":Project.objects.filter(project_admin=request.user).count(),
                "TC":Task.objects.filter(user_name=request.user).count(),
                "GC":Groups_Members.objects.filter(group_member=request.user).count(),
                "FC":Friend.objects.filter(friend_of=request.user).count(),
                "Friend":Friend.objects.filter(friend_of=user),
                "Task":Task.objects.filter(task_project_id=proid),
                "FR":tot})


def addfriend(request):
        user=request.user
        fr=Friend_Request.objects.filter(friend_is=request.user).count()
        gr=Groups_Request.objects.filter(group_member=request.user).count()
        tot=fr+gr
        if request.method=='POST':
                friend=request.POST['fname']
                if User.objects.filter(username=friend).exists():
                        if Friend.objects.filter(friend_of=user.username,friend_is=friend).exists():
                                return redirect('addfriend')
                        else:
                                fri=Friend_Request.objects.create()
                                fri.friend_of=user.username
                                fri.friend_is=friend
                                fri.save()
                                return redirect('friends')
                        
        return render(request,'addfriend.html',context={
                "Project":Project.objects.filter(project_admin=user),
                "PC":Project.objects.filter(project_admin=request.user).count(),
                "TC":Task.objects.filter(user_name=request.user).count(),
                "GC":Groups_Members.objects.filter(group_member=request.user).count(),
                "FC":Friend.objects.filter(friend_of=request.user).count(),
                "FR":tot})

def addgroup(request):
        user=request.user
        fr=Friend_Request.objects.filter(friend_is=request.user).count()
        gr=Groups_Request.objects.filter(group_member=request.user).count()
        tot=fr+gr
        if request.method=='POST':
                gname=request.POST['gname']
                grp=Groups.objects.create()
                grp.group_name=gname
                grp.group_admin=user.username
                grp.save()
                mem=Groups_Members.objects.create()
                mem.group_id=grp.group_id
                mem.group_name=gname
                mem.group_member=user.username
                mem.save()
                request.session['grpid']=grp.group_id
                return redirect('addmember')
        return render(request,'addgroup.html',context={
                "Project":Project.objects.filter(project_admin=user),
                "PC":Project.objects.filter(project_admin=request.user).count(),
                "TC":Task.objects.filter(user_name=request.user).count(),
                "GC":Groups_Members.objects.filter(group_member=request.user).count(),
                "FC":Friend.objects.filter(friend_of=request.user).count(),
                "FR":tot})

def addmember(request):
        user=request.user
        fr=Friend_Request.objects.filter(friend_is=request.user).count()
        gr=Groups_Request.objects.filter(group_member=request.user).count()
        tot=fr+gr
        grp_id=request.session['grpid']
        if request.method=='POST':
                member=request.POST['mname']
                if Groups_Members.objects.filter(group_id=grp_id,group_member=member).exists():
                        return redirect('addmember')
                if Groups_Request.objects.filter(group_id=grp_id,group_member=member,group_admin=user).exists():
                        return redirect('addmember')
                else:
                        grp=Groups_Request.objects.create()
                        grp.group_id=grp_id
                        grp.group_admin=user.username
                        grp.group_member=member
                        grp.save()
                        return redirect('addmember')
        return render(request,'addmember.html',context={
                "Project":Project.objects.filter(project_admin=user),
                "PC":Project.objects.filter(project_admin=request.user).count(),
                "TC":Task.objects.filter(user_name=request.user).count(),
                "GC":Groups_Members.objects.filter(group_member=request.user).count(),
                "FC":Friend.objects.filter(friend_of=request.user).count(),
                "Friends":Friend.objects.filter(friend_of=request.user),
                "Group":Groups_Members.objects.filter(group_id=grp_id),
                "FR":tot})
