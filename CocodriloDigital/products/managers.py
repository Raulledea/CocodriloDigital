"""Managers customizados para modelos.

Optimiza queries y proporciona métodos convenientes para acceder a datos.
"""
from django.db import models
from django.utils import timezone


class ActivePromotionManager(models.Manager):
    """Manager para consultas de promociones activas."""
    
    def active(self):
        """Retorna solo promociones activas (en rango de fechas).
        
        Returns:
            QuerySet: Promociones con fecha/hora actual en rango [start_date, end_date].
        """
        now = timezone.now()
        return self.filter(start_date__lte=now, end_date__gte=now)
    
    def upcoming(self):
        """Retorna solo promociones futuras.
        
        Returns:
            QuerySet: Promociones cuya fecha de inicio es posterior a ahora.
        """
        now = timezone.now()
        return self.filter(start_date__gt=now)
    
    def expired(self):
        """Retorna solo promociones vencidas.
        
        Returns:
            QuerySet: Promociones cuya fecha de fin es anterior a ahora.
        """
        now = timezone.now()
        return self.filter(end_date__lt=now)


class ProductWithDiscountManager(models.Manager):
    """Manager para productos con optimizaciones comunes."""
    
    def with_discounts(self):
        """Retorna productos que tienen promociones activas.
        
        Returns:
            QuerySet: Productos con al menos una promoción activa, optimizado.
        """
        now = timezone.now()
        return self.filter(
            promotions__start_date__lte=now,
            promotions__end_date__gte=now
        ).prefetch_related('promotions', 'category').distinct()
    
    def by_category(self):
        """Retorna productos agrupados optimizadamente por categoría.
        
        Returns:
            QuerySet: Productos con category prefetch_related.
        """
        return self.prefetch_related('category', 'promotions').select_related('category')
