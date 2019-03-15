from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, TeamForm, TaskForm, TaskEditForm, CommentForm
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.contrib.auth.models import Group, User
import simplejson as json
from .models import Team, Task, Comments
from django.contrib.auth.decorators import login_required
from django import forms
from django.utils import timezone

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

"""

Home View where the current user can get all the information like
-> In which teams he is a member
-> Teams created by him
-> Tasks created by him
-> Tasks assigned to him
-> Tasks of his team

"""

def home(request):
    if request.user.is_anonymous:
        return render(request,'home.html')
    teams = [team for team in Team.objects.all() if request.user in team.users.all()]
    teams_created = [team for team in Team.objects.all() if request.user == team.created_by]
    tasks_created = [task for task in Task.objects.all() if request.user == task.created_by]
    tasks_assigned = [task for task in Task.objects.all() if request.user == task.assignee]
    my_team_tasks = []
    for team in teams:
        for task in Task.objects.all():
            if task.team == team:
                my_team_tasks.append(task)
    return render(request,'home.html', {'teams': teams,'teams_created': teams_created, 'tasks_created': tasks_created,'tasks_assigned': tasks_assigned,'my_team_tasks': my_team_tasks})

@login_required
def users_list(request):
    username = request.GET.get('username', None)
    id = request.user.id
    user = User.objects.filter(id=id)
    all_users = User.objects.all().order_by('id').exclude(id=id)
    return JsonResponse({
            'results': [
                #{'text': str(obj.username)}
                {'id': str(obj.id), 'text': str(obj.username)}
                for obj in all_users
            ],
        })

"""
Team registration ## only authenticated users can do it
"""

@login_required
def teamreg(request):
    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            users = form.cleaned_data['users']
            teamtitle = request.POST.get('title')
            team = form.save(commit=False)
            team = Team.objects.create()
            team.title = teamtitle
            for user in users:
                team.users.add(user)
            team.users.add(request.user)
            team.created_by = request.user
            team.save()
            return redirect('home')
        else:
            return HttpResponse('form invalid')
    else:
        form = TeamForm()
    return render(request, 'registration/team.html', {'form': form})

"""
View to edit team and render the updated team
"""

def teamedit(request, string):
    team = get_object_or_404(Team, title=string)
    if str(request.user) != str(team.created_by):
        return HttpResponse("You don't have permission to edit")
    if request.method == "POST":
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            users = form.cleaned_data['users']
            teamtitle = request.POST.get('title')
            team.title = teamtitle
            team.users.clear()
            for user in users:
                if str(user)!=str(request.user):
                    team.users.add(user)
            team.users.add(request.user)
            team.save()
            return redirect('teamview', string=team.title)
    else:
        form = TeamForm(instance=team)
    return render(request, 'registration/teamedit.html', {'form': form})

'''
Get the team and check if request.user is team creator or not by using see variable.
'''

def teamview(request, string):
    team = get_object_or_404(Team, title=string)
    if team is None:
        return HttpResponse("Team not found")
    if str(request.user) == str(team.created_by):
        see = 1
    else:
        see = 0
    teammates = [val for val in team.users.all() if val in team.users.all()]
    return render(request, 'teamview.html', {'team': team, 'teammates': teammates, 'see': see})

# ajax to fetch users list of a team in task creation page  
@login_required
def team_users_list(request):
    id = request.GET.get('team', None)
    team = get_object_or_404(Team, id=id)
    all_users = [val for val in team.users.all() if val in team.users.all()]
    data = {
            str(obj.id) : str(obj.username)
            for obj in all_users
        },
    print(json.dumps(data))
    return JsonResponse(data,safe=False)

# teams list as ajax to fetch teams list where the user is member # team creator is also a member
@login_required
def teams_list(request):
    teams = [team for team in Team.objects.all() if request.user in team.users.all()]
    all_teams = teams
    data = {
            str(obj.id) : str(obj.title)
            for obj in all_teams
        },
    print(json.dumps(data))
    return JsonResponse(data,safe=False)


@login_required
def taskreg(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            tasktitle = request.POST.get('title')
            desc = request.POST.get('description')
            teamid = request.POST.get('team')
            asignes = form.cleaned_data['assignee']
            state = request.POST.get('status')
            created_by = request.user
            created_at = timezone.now()
            last_modified = timezone.now()

            # if team is empty then assignee has to be the request.user always
            if teamid=="":
                Task.objects.create(title=tasktitle,description=desc,created_by=created_by,status=state,created_at=created_at,last_modified=last_modified)
                task = get_object_or_404(Task, title=tasktitle)
                task.assignee.add(request.user)
                return redirect('taskview', string=task.title)
            else:
                team = Team.objects.get(id=teamid)
                # no assignee at present we'll add later
                Task.objects.create(title=tasktitle,description=desc,created_by=created_by,team=team,status=state,created_at=created_at,last_modified=last_modified)
            task = get_object_or_404(Task, title=tasktitle)
            #So, we have a team assigned for task
            for user in asignes:
                task.assignee.add(user)
            task.save()
            return redirect('taskview', string=task.title)
        else:
            return HttpResponse('form invalid')
    else:
        form = TaskForm(request.user)
    return render(request, 'task.html', {'form': form})



"""
View to edit task and render the updated task
"""
@login_required
def taskedit(request, string):
    task = get_object_or_404(Task, title=string)
    taskprev = task
    if str(request.user) != str(task.created_by):
        return HttpResponse("You don't have permission to edit")
    if request.method == "POST":
        form = TaskEditForm(request.POST, instance=task)
        # no assignee 
        if(request.POST.get('assignee')==""):
            task.assignee.clear()
            tasktitle = request.POST.get('title')
            taskdesc = request.POST.get('description')
            task.title = tasktitle
            task.description = taskdesc

            state = request.POST.get('status')
            task.status = state
            task.last_modified = timezone.now()
            task.save()
            comm = Comments.objects.filter(task = taskprev)
            # changing comments related to task when task is changed
            for com in comm:
                com.task = task
                com.save()
            return redirect('taskview', string=task.title)         
        # assignee is there
        if form.is_valid():
            tasktitle = request.POST.get('title')
            taskdesc = request.POST.get('description')
            task.title = tasktitle
            task.description = taskdesc
            #asigne = request.POST.get('assignee')
            #                 
            if(request.POST.get('assignee')==""):
                task.assignee.clear()
            else:
                asignes = form.cleaned_data['assignee']
                task.assignee.clear()
                for user in asignes:
                    task.assignee.add(user)
            state = request.POST.get('status')
            task.status = state
            task.last_modified = timezone.now()
            task.save()
            comm = Comments.objects.filter(task = taskprev)
            # changing comments related to task when task is changed
            for com in comm:
                com.task = task
                com.save()
            return redirect('taskview', string=task.title)
        else:
            return HttpResponse("form invalid")
    else:
        form = TaskEditForm(instance=task)
        team = get_object_or_404(Team, id=task.team.id)
        users = [val for val in team.users.all() if val in team.users.all()]
        assignes = task.assignee
        a = [val for val in task.assignee.all() if val in task.assignee.all()]
    return render(request, 'taskedit.html', {'form': form, 'task': task, 'users': users, 'a': a})


"""
View which allows specific users to view the task 
"""
@login_required
def taskview(request, string):
    task = get_object_or_404(Task, title=string)
    if task is None:
        return HttpResponse("Task not found")
    
    if task.team is None:
        # has permission to see
        if request.user == task.created_by:
            if request.method == "POST":
                form = CommentForm(request.POST)
                if form.is_valid():
                    task = get_object_or_404(Task, title=string)
                    comment = request.POST.get('comment')
                    created_by = request.user
                    created_at = timezone.now()
                    Comments.objects.create(task=task,author=created_by,comment=comment,created_date=created_at)
                    task = get_object_or_404(Task, title=string)
                else:
                    return HttpResponse('comment invalid')
            c = Comments.objects.all().filter(task=task)
            comments = [comment for comment in c]
            form = CommentForm()
            return render(request, 'taskview.html', {'form': form,'task': task,'comments': comments})
        else:
            # sorry no permission
            return HttpResponse("You don't have permission to see the task")
    # team exists so team mates can see the task

    team = get_object_or_404(Team, id=task.team.id)
    users = [val for val in team.users.all() if val in team.users.all()]
    if request.user in users:
        # has permission to see
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                task = get_object_or_404(Task, title=string)
                comment = request.POST.get('comment')
                created_by = request.user
                created_at = timezone.now()
                Comments.objects.create(task=task,author=created_by,comment=comment,created_date=created_at)
                task = get_object_or_404(Task, title=string)
            else:
                return HttpResponse('comment invalid')
        c = Comments.objects.all().filter(task=task)
        comments = [comment for comment in c]
        assignes = task.assignee
        a = [val for val in task.assignee.all() if val in task.assignee.all()]
        form = CommentForm()
        return render(request, 'taskview.html', {'form': form,'task': task,'comments': comments,'a':a})
    else:
        # sorry no permission
        return HttpResponse("You don't have permission to see the task")


"""
View to delete Task along with its comments
"""
@login_required
def taskdelete(request, string):
    task = get_object_or_404(Task, title=string)
    if task is None:
        return HttpResponse("Task not found")
    if request.user == task.created_by:
        # has permission to delete task
        comments = Comments.objects.all().filter(task=task)
        if comments is not None: # if comments exists then delete
            for comment in comments:
                comment.delete()
        task.delete()
        return redirect('home')
    else:
        # sorry no permission
        return HttpResponse("You don't have permission to delete the task")



"""
View to Create Comment for a specific task created in a same group
"""
@login_required
def commentreg(request,string):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            task = get_object_or_404(Task, title=string)
            comment = request.POST.get('comment')
            created_by = request.user
            created_at = timezone.now()
            Comments.objects.create(task=task,author=created_by,comment=comment,created_by=created_by,assignee=assignee,status=state,created_at=created_at,last_modified=last_modified)
            task = get_object_or_404(Task, title=string)
            #return taskview(request, string)
            return redirect('taskview', string=string)
        else:
            return HttpResponse('comment invalid')
    else:
        form = CommentForm()
    return taskview(request, string)


"""
View to Edit Comment  ### allows only comment creator to edit ###
"""
@login_required
def commentedit(request, id):
    comment = get_object_or_404(Comments, id=id)
    if str(request.user) != str(comment.author):
        return HttpResponse("You don't have permission to edit")
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            task = get_object_or_404(Task, title=comment.task)
            new_comment = request.POST.get('comment')
            comment.comment = new_comment
            comment.save()
            return redirect('taskview', string=task.title)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'commentedit.html', {'form': form, 'comment': comment})

"""
View to Delete Comment ### allows only comment creator to delete ###
"""
@login_required
def commentdel(request, id):
    comment = get_object_or_404(Comments, id=id)
    if str(request.user) != str(comment.author):
        # has no permission
        return HttpResponse("You don't have permission to delete Comment contact comment creator")
    else:
        # has permission to delete
        task = comment.task
        comment.delete()
        return redirect('taskview', string=task.title)

