from django import forms


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