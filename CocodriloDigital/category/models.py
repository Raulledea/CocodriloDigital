"""Modelos de la aplicación 'category'.

Contiene las categorías de productos con soporte para subcategorías.
"""
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """Modelo de categoría de productos.
    
    Soporta categorías jerárquicas (padre-hijo).
    
    Atributos:
        name (str): Nombre de la categoría.
        slug (str): Identificador URL único (autogenerado de name).
        description (str): Descripción opcional de la categoría.
        parent (Category): Referencia opcional a categoría padre para subcategorías.
    """
    name = models.CharField(max_length=100, help_text="Nombre de la categoría")
    slug = models.SlugField(unique=True, blank=True, help_text="URL amigable (autogenerada)")
    description = models.TextField(blank=True, null=True, help_text="Descripción opcional")
    # Relación reflexiva para soportar subcategorías
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        """Retorna el nombre de la categoría."""
        return self.name
    
    def save(self, *args, **kwargs):
        """Genera automáticamente el slug si no existe."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)