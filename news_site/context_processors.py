from .models import Category


def global_context(request):
    categories = Category.objects.all()
    is_journalist = False
    is_admin = False
    
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.groups.filter(name='Admin').exists():
            is_admin = True
            is_journalist = True
        elif request.user.groups.filter(name='Journalist').exists():
            is_journalist = True
            
    return {
        'categories': categories,
        'is_journalist': is_journalist,
        'is_admin': is_admin,
    }
