from .models import Category


def global_context(request):
    """Inject global context variables into every template."""
    categories = Category.objects.all()
    return {
        'categories': categories,
    }
