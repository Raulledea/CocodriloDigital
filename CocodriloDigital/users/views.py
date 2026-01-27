"""Vistas de autenticación de usuarios.

Contiene las vistas para login, logout, registro y gestión de sesiones.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm


@require_http_methods(["GET", "POST"])
def login_view(request):
    """Vista para iniciar sesión con validaciones.
    
    GET: Muestra el formulario de login.
    POST: Procesa las credenciales y autentica al usuario.
    
    Args:
        request: La solicitud HTTP.
        
    Returns:
        HttpResponse: El formulario de login o redirección tras autenticarse.
    """
    # Si ya está autenticado, redirige al home
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        if not username or not password:
            messages.error(request, 'Por favor ingresa usuario y contraseña.')
            return render(request, 'auth/login.html')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    return render(request, 'auth/login.html')


@require_http_methods(["POST"])
def logout_view(request):
    """Vista para cerrar sesión.
    
    Cierra la sesión del usuario autenticado y redirige al home.
    Solo acepta POST por seguridad (CSRF protection).
    
    Args:
        request: La solicitud HTTP.
        
    Returns:
        HttpResponse: Redirección al home.
    """
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('home')


@require_http_methods(["GET", "POST"])
def register_view(request):
    """Vista para registrar un nuevo usuario con validaciones.
    
    GET: Muestra el formulario de registro.
    POST: Procesa el formulario y crea un nuevo usuario si es válido.
    
    Args:
        request: La solicitud HTTP.
        
    Returns:
        HttpResponse: El formulario de registro o redirección tras registrarse.
    """
    # Si ya está autenticado, redirige al home
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, 
                f'¡Bienvenido {user.username}! Tu cuenta ha sido creada exitosamente.'
            )
            return redirect('home')
        else:
            # Los errores del formulario se mostrarán en la plantilla
            pass
    else:
        form = RegisterForm()
    
    return render(request, 'auth/register.html', {'form': form})
