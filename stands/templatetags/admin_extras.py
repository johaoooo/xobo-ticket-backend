from django import template
from stands.models import Stand
from users.models import User
from django.utils import timezone
from datetime import timedelta

register = template.Library()

@register.simple_tag
def get_total_stands():
    return Stand.objects.count()

@register.simple_tag
def get_valides_stands():
    return Stand.objects.filter(statut='valide').count()

@register.simple_tag
def get_attente_stands():
    return Stand.objects.filter(statut='en_attente').count()

@register.simple_tag
def get_total_users():
    return User.objects.count()

@register.simple_tag
def get_recent_stands():
    return Stand.objects.all().order_by('-created_at')[:5]

@register.simple_tag
def get_monthly_stats():
    months = []
    monthly_counts = []
    now = timezone.now()
    
    for i in range(5, -1, -1):
        month = now - timedelta(days=30*i)
        month_start = month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        month_end = (month_start + timedelta(days=32)).replace(day=1)
        
        count = Stand.objects.filter(created_at__gte=month_start, created_at__lt=month_end).count()
        
        months.append(month_start.strftime('%b %Y'))
        monthly_counts.append(count)
    
    return {
        'months': months,
        'counts': monthly_counts,
    }
