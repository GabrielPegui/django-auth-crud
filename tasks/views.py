from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.db import IntegrityError
from .forms import taskform
from .models import task
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(response):
    usuarios_hoy = User.objects.all()
    return render(response,'home.html',{'all_users': usuarios_hoy})

def singup(response):

    if response.method == 'GET':
       return render(response,'singup.html',{'form' : UserCreationForm })
    else:
      if response.POST['password1'] == response.POST['password2']:
            # register user
            try:
                new_user = User.objects.create_user(username=response.POST['username'],password=response.POST['password1'])
                new_user.save()
                login(response,new_user)
                return redirect('task')
            except IntegrityError:
                 return render(response,'singup.html',{'form' : UserCreationForm , 'error': 'user already exists'})

        
      else:
           return render(response,'singup.html',{'form' : UserCreationForm , 'error': 'passwords do not match'})
      
@login_required
def tasks(response):

    task2 = task.objects.filter(user=response.user,datecompleted__isnull=True)

    return render(response,'task.html',{ 'tasks': task2 })  

@login_required
def singout(response):
    logout(response)
    return redirect('home')

def login_user(response):
    if response.method == 'GET':
       return render(response,'login_user.html',{ 'form': AuthenticationForm})
    else:
        user = authenticate(response,username=response.POST['username'],password=response.POST['password'])

        if user is None:
            return render(response,'login_user.html',{ 'form': AuthenticationForm, 'error': 'username o password incorrect'})
        else:
            login(response,user)
            return redirect('task')
        
@login_required    
def create_task(response):
    if response.method == 'GET':
         return render(response,'create_task.html',{ 'form': taskform})
    else:
         try:
            form = taskform(response.POST)
            new_task = form.save(commit=False)
            new_task.user = response.user
            new_task.save()
            return redirect('task')
         except ValueError:
             return render(response,'create_task.html',{ 'form': taskform, 'error': 'please provide valida data'})
         
@login_required       
def task_detail(response,task_id):
    if response.method == 'GET':
        task_d = get_object_or_404(task,pk=task_id,user=response.user)
        form = taskform(instance=task_d)
        return render(response,'task_detail.html',{'task': task_d , 'form':form})
    else:

        try:
            task_d = get_object_or_404(task,pk=task_id, user=response.user)
            form = taskform(response.POST,instance=task_d)
            form.save()
            return redirect('task')
        except ValueError:
            return render(response,'task_detail.html',{'task': task_d , 'form':form, 'error': 'error updating task'})
        
@login_required       
def task_complete(response,task_id):
    task_d = get_object_or_404(task,pk=task_id,user=response.user)
    if response.method == 'POST':
       task_d.datecompleted = timezone.now()
       task_d.save()
       return redirect('task')

@login_required
def task_delete(response,task_id):
    task_d = get_object_or_404(task,pk=task_id,user=response.user)
    if response.method == 'POST':
        task_d.delete()

   
    return redirect('task')

@login_required
def task_finished(response):
    task2 = task.objects.filter(user=response.user,datecompleted__isnull=False)

    return render(response,'task_finished.html',{ 'tasks': task2 })  

        
        



   





         
