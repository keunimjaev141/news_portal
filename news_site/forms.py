from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User as AuthUser
from .models import NewsArticle, Category

class ArticleForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Maqola sarlavhasi'
        })
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'placeholder': 'Maqola matni...',
            'rows': 10
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label='Kategoriya tanlang'
    )
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-input'})
    )

class RegisterForm(UserCreationForm):
    class Meta:
        model = AuthUser
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'


class CommentForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ismingiz'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Email manzilingiz'
        })
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'placeholder': 'Izohingizni yozing...',
            'rows': 4
        })
    )


class SubscribeForm(forms.Form):
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('basic', 'Basic'),
        ('premium', 'Premium'),
    ]
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'To\'liq ismingiz'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Email manzilingiz'
        })
    )
    plan_type = forms.ChoiceField(
        choices=PLAN_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )