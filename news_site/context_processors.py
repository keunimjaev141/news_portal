from .models import Category


def global_context(request):
    categories = Category.objects.all()
    return {
        'categories': categories,
    }
