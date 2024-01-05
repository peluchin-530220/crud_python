from django.shortcuts import render, redirect,get_object_or_404,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import tareaForm
from .models import tarea
from django.utils import timezone
from django.contrib.auth.decorators import login_required



# Create your views here.
def index(request):
    return render(request, "index.html")


def registrate(request):

    if request.method == "GET":
        return render(request, "registrate.html")
    else:
        if request.POST["password2"] == request.POST["password1"]:
            # registrar usuario
            try:
                user = User.objects.create_user(username=request.POST["username"],
                password=request.POST["password1"])
                user.save()
                login(request,user)
                return redirect("tarea")
            except IntegrityError:
                return render(request, "registrate.html", {
                    "error": "el usuario ya existe"
                })

        return render(request, "registrate.html", {
            "error": "contraceña no coincide"
        })

@login_required
def tarea_list(request):
    tareas = tarea.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request,"tarea.html", {"tareas":tareas})

@login_required
def crear_tarea(request):
    if request.method == "GET":
        return render(request, "crear_tarea.html",{
        "form": tareaForm
    })
    else:
        try:
            form = tareaForm(request.POST)
            nueva_tarea = form.save(commit=False)
            nueva_tarea.user = request.user
            nueva_tarea.save()
            return redirect("tarea")
        except ValueError:
                return render(request, "crear_tarea.html",{
                "form": tareaForm,
                "error": "porfavor provee datos validos"
            })
        
#  ACTUALIZA LAS TAREAS 
@login_required
def detalles_tarea(request, tarea_id):
    tarea_obj = get_object_or_404(tarea, pk=tarea_id, user=request.user)
    if request.method == "GET":
        form = tareaForm(instance=tarea_obj)
        return render(request, "detalles_tarea.html", {"tarea": tarea_obj, "form": form})
    else:
        form = tareaForm(request.POST, instance=tarea_obj)  # Utiliza tarea_obj en lugar de tarea
        if form.is_valid():
            form.save()  # Guarda los cambios en la instancia
            return redirect("tarea")
        else:
            # Si el formulario no es válido, puedes manejar el caso de error aquí
            return render(request, "detalles_tarea.html", {"tarea": tarea_obj, "form": form})

# COMPLETA LA TAREA (elimina)
@login_required
def completa_tarea(request, tarea_id):
    tarea_obj = get_object_or_404(tarea, pk=tarea_id, user=request.user)

    if request.method == "POST":
        # Marcar la tarea como completa (establecer la fecha de completado)
        tarea_obj.datecompleted = timezone.now()
        tarea_obj.save()
        return redirect("tarea")
    
# ELIMINA LA TAREA USANDO OTRO URL
def eliminar_tarea(request, tarea_id):
    tarea_obj = get_object_or_404(tarea, pk=tarea_id, user=request.user)

    if request.method == "POST":
        tarea_obj.delete()
        return redirect("tarea")
    
# VISTA DE TODAS LAS TAREAS COMPLETADAS
@login_required    
def tarea_completas(request):
    tareas = tarea.objects.filter(user=request.user, datecompleted__isnull=False).order_by
    ("-datecompleted")
    return render(request,"tarea.html", {"tareas":tareas})

def cerrar_sesion(request):
    logout(request)
    return redirect("index")

def iniciar_sesion(request):
    if request.method == "GET":
        return render(request, "iniciar_sesion.html")
    else:
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        if user is None:
            return render(request, "iniciar_sesion.html",{
            "error": "ususario o contraceña incorrecto"
            })
        else:
            login(request, user)
            return redirect("tarea")
            
       

    
