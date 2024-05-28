# Create your views here. 
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.timezone import now, localtime
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm

# Create your views here.

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                usuario = User.objects.create_user(request.POST["username"], password=request.POST["password1"])
                usuario.save()
                login(request, usuario)
                return redirect('tasks') 
            except IntegrityError:
                return render(request, 'signup.html', {"form": UserCreationForm, "error": "Usuario " + request.POST["username"] + " ya existe"})
        return render(request, 'signup.html', {"form": UserCreationForm, "error": "Las contraseñas no son iguales"})
    
def home(request):
    return render(request, 'home.html', {})

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm})
    else:
        usuario = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if usuario is None:
            return render(request, 'signin.html', {"form": AuthenticationForm, "error": "Usuario o contraseña incorrecta."})

        login(request, usuario)
        return redirect('tasks')
    
#CRUD - LOGIN REQUERIDO
@login_required
def tasks(request):
    tasks = Task.objects.filter(usuario=request.user)  
    return render(request, 'tasks.html', {"tasks": tasks})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'tasks.html', {"tasks": tasks})


@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, 'form_create_task.html', {"form": TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.usuario = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'form_create_task.html', {"form": TaskForm, "error": "Error inesperado creando la tarea"})


@login_required
def signout(request):
    logout(request)
    return redirect('home')

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, usuario=request.user)
        form = TaskForm(instance=task)  
        return render(request, 'form_detail_task.html', {'task': task, 'form': form,  'is_completed': task.completada, 'disabled_class': 'disabled' if task.completada else '', 'title_class': 'text-decoration-line-through' if task.completada else ''})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, usuario=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'form_detail_task.html', {'task': task, 'form': form, 'error': 'Error inesperado actualizando la tarea'})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, usuario=request.user)  
    if request.method == 'POST':
        task.fecha_completada = localtime(now()) 
        task.completada = True
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, usuario=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    
#CRUD - LOGIN REQUERIDO