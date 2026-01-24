from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.db import IntegrityError


@require_http_methods(["GET", "POST"])
def login_view(request):
    """Vista para el login de usuarios."""
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        
        # Autenticar usuario
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Login exitoso
            login(request, user)
            
            # Mantener sesión abierta si el usuario marca "Recordarme"
            if not remember:
                request.session.set_expiry(0)
            
            return redirect('home')  # Redirigir a la página principal
        else:
            # Login fallido
            context = {
                'error': 'Usuario o contraseña incorrectos',
                'username': username
            }
            return render(request, 'login/login.html', context)
    
    return render(request, 'login/login.html')


@require_http_methods(["GET", "POST"])
def register_view(request):
    """Vista para el registro de nuevos usuarios."""
    if request.method == "POST":
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        username = request.POST.get('username', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        
        errors = []
        
        # Validaciones
        if not full_name:
            errors.append("El nombre completo es requerido")
        if not email:
            errors.append("El correo es requerido")
        if not username:
            errors.append("El usuario es requerido")
        if len(username) < 3:
            errors.append("El usuario debe tener al menos 3 caracteres")
        if len(password1) < 8:
            errors.append("La contraseña debe tener al menos 8 caracteres")
        if password1 != password2:
            errors.append("Las contraseñas no coinciden")
        
        # Validar que el usuario no exista
        if User.objects.filter(username=username).exists():
            errors.append("El usuario ya existe")
        if User.objects.filter(email=email).exists():
            errors.append("El correo ya está registrado")
        
        if errors:
            context = {
                'errors': errors,
                'full_name': full_name,
                'email': email,
                'username': username
            }
            return render(request, 'login/register.html', context)
        
        # Crear usuario
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=full_name.split()[0] if full_name else '',
                last_name=' '.join(full_name.split()[1:]) if len(full_name.split()) > 1 else ''
            )
            
            # Login automático después del registro
            login(request, user)
            return redirect('home')
        except IntegrityError:
            context = {
                'errors': ['Error al crear la cuenta. Intenta de nuevo.'],
                'full_name': full_name,
                'email': email,
                'username': username
            }
            return render(request, 'login/register.html', context)
    
    return render(request, 'login/register.html')
