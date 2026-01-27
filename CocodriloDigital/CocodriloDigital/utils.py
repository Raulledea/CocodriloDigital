"""Utilidades compartidas para toda la aplicación.

Contiene decoradores, funciones helper y utilidades generales.
"""
from functools import wraps
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.shortcuts import redirect


def superuser_required(login_url='users:login'):
    """Decorador para requerir permisos de superusuario.
    
    Si el usuario no es superusuario, redirige a home con un mensaje de error.
    Si no está autenticado, redirige a login.
    
    Args:
        login_url (str): URL a la que redirigir si no está autenticado.
    
    Returns:
        function: Decorador que envuelve la vista.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(login_url)
            
            if not request.user.is_superuser:
                messages.error(request, 'No tienes permiso para acceder a esta página.')
                return redirect('home')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def is_superuser(user):
    """Verifica si un usuario es superusuario.
    
    Utilizada en decoradores como @user_passes_test.
    
    Args:
        user: Objeto de usuario de Django.
    
    Returns:
        bool: True si el usuario es superusuario, False en caso contrario.
    """
    return user.is_superuser
