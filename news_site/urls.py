from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('category/<int:pk>/', views.category_articles, name='category_articles'),
    path('journalist/<int:pk>/', views.journalist_detail, name='journalist_detail'),
    path('search/', views.search, name='search'),
    path('subscribe/', views.subscribe, name='subscribe'),
]
