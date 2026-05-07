from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import NewsArticle, Category, Comment, User, Journalist, Advertisement, Subscription
from .forms import CommentForm, SubscribeForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User as AuthUser
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required

def register_view(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    return render(request, 'register.html', {'form': form})

def login_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


def home(request):
    articles = NewsArticle.objects.select_related('category', 'author').all()[:12]
    categories = Category.objects.all()
    featured = NewsArticle.objects.order_by('-views').first()
    latest = NewsArticle.objects.order_by('-published_date')[:5]
    ads = Advertisement.objects.all()[:3]
    context = {
        'articles': articles,
        'categories': categories,
        'featured': featured,
        'latest': latest,
        'ads': ads,
    }
    return render(request, 'home.html', context)


def article_detail(request, pk):
    article = get_object_or_404(NewsArticle, pk=pk)
    article.views += 1
    article.save()
    comments = article.comments.select_related('user').all()
    related = NewsArticle.objects.filter(category=article.category).exclude(pk=pk)[:4]
    ads = Advertisement.objects.filter(article=article)
    comment_form = CommentForm()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            name = comment_form.cleaned_data['name']
            email = comment_form.cleaned_data['email']
            content = comment_form.cleaned_data['content']
            user, _ = User.objects.get_or_create(email=email, defaults={'name': name})
            Comment.objects.create(user=user, article=article, content=content)
            return redirect('article_detail', pk=pk)
    context = {
        'article': article,
        'comments': comments,
        'related': related,
        'comment_form': comment_form,
        'ads': ads,
    }
    return render(request, 'article_detail.html', context)


def category_articles(request, pk):
    category = get_object_or_404(Category, pk=pk)
    articles = NewsArticle.objects.filter(category=category).select_related('author')
    categories = Category.objects.all()
    context = {
        'category': category,
        'articles': articles,
        'categories': categories,
    }
    return render(request, 'category.html', context)


def journalist_detail(request, pk):
    journalist = get_object_or_404(Journalist, pk=pk)
    articles = NewsArticle.objects.filter(author=journalist).order_by('-published_date')
    context = {
        'journalist': journalist,
        'articles': articles,
    }
    return render(request, 'journalist.html', context)


def search(request):
    query = request.GET.get('q', '')
    articles = []
    if query:
        articles = NewsArticle.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).select_related('category', 'author')
    context = {
        'articles': articles,
        'query': query,
        'categories': Category.objects.all(),
    }
    return render(request, 'search.html', context)


def subscribe(request):
    form = SubscribeForm()
    success = False
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            plan = form.cleaned_data['plan_type']
            user, _ = User.objects.get_or_create(email=email, defaults={'name': name})
            Subscription.objects.create(user=user, plan_type=plan)
            success = True
    context = {'form': form, 'success': success}
    return render(request, 'subscribe.html', context)