from datetime import date
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Book, Author


class BookForm(forms.ModelForm):
    author_search = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(attrs={"placeholder": "Search author / Hľadať autora", "class": "author-search-input"})
    )
    title = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder": "Title / Názov"}))
    isbn = forms.CharField(
        label='',
        min_length=13,
        max_length=13,
        widget=forms.TextInput(attrs={
            "placeholder": "ISBN - International Standard Book Number / Medzinárodné štandardné číslo knihy",
            "inputmode": "numeric",
            "pattern": "[0-9]{13}",
            "maxlength": "13",
        })
    )
    year = forms.IntegerField(label='', widget=forms.NumberInput(attrs={"min": 0, "max": date.today().year, "step": 1, "placeholder": "Publication year / Rok vydania"}))
    total_copies = forms.IntegerField(label='', min_value=0, widget=forms.NumberInput(attrs={"min": 0, "step": 1, "placeholder": "All copies / Všetky kópie"}))

    class Meta:
        model = Book
        fields = ['title', 'isbn', 'genre', 'year', 'total_copies', 'authors', 'cover_image']
        labels = {
            'title': '',
            'isbn': '',
            'genre': '',
            'year': '',
            'total_copies': '',
            'cover_image': 'Book cover / Obálka knihy',
            'authors': '',
        }
        widgets = {
            'genre': forms.Select(choices=[('', 'Genre / Žáner')] + Book.GENRE_CHOICES),
            'authors': forms.SelectMultiple(attrs={"class": "author-select", "size": "8"}),
            'cover_image': forms.ClearableFileInput(attrs={"class": "cover-input"}),
        }

    def clean_isbn(self):
        isbn = (self.cleaned_data.get('isbn') or '').strip()
        if not isbn.isdigit() or len(isbn) != 13:
            raise ValidationError('ISBN must contain exactly 13 digits. / ISBN musí obsahovať presne 13 číslic.')
        qs = Book.objects.filter(isbn=isbn)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError('A book with this ISBN already exists. / Kniha s týmto ISBN už existuje.')
        return isbn


class AuthorForm(forms.ModelForm):
    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'First name / Meno'}))
    last_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Last name / Priezvisko'}))
    birth_date = forms.DateField(label='', widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Birth date / Dátum narodenia'}))
    country = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Country / Krajina'}))
    description = forms.CharField(label='', required=False, widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Description / biography / Popis / životopis'}))

    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'birth_date', 'country', 'description']


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False, label='', widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'username': '', 'email': '', 'password1': '', 'password2': ''}
        help_texts = {'username': '', 'email': '', 'password1': '', 'password2': ''}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'username': 'Username / Meno',
            'email': 'Email',
            'password1': 'Password / Heslo',
            'password2': 'Repeat password / Zopakuj heslo',
        }
        for name, field in self.fields.items():
            field.label = ''
            field.help_text = ''
            field.widget.attrs.update({'placeholder': placeholders.get(name, ''), 'class': 'auth-input'})


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Username / Používateľské meno',
            'first_name': 'First name / Meno',
            'last_name': 'Last name / Priezvisko',
            'email': 'Email',
        }
        help_texts = {
            'username': '',
            'first_name': '',
            'last_name': '',
            'email': '',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'username': 'Username / Používateľské meno',
            'first_name': 'First name / Meno',
            'last_name': 'Last name / Priezvisko',
            'email': 'Email',
        }
        for name, field in self.fields.items():
            field.label = ''
            field.help_text = ''
            field.widget.attrs.update({'placeholder': placeholders.get(name, ''), 'class': 'profile-input'})


class AdminUserEditForm(forms.ModelForm):
    password = forms.CharField(required=False, label='New password / Nové heslo', widget=forms.PasswordInput(attrs={'placeholder': 'Fill in only if you want to change the password / Vyplň iba ak chceš zmeniť heslo'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active']
        labels = {
            'username': 'Username / Používateľské meno',
            'first_name': 'First name / Meno',
            'last_name': 'Last name / Priezvisko',
            'email': 'Email',
            'is_staff': 'Admin account / Admin účet',
            'is_active': 'Active account / Aktívny účet (inactive account is suspended / neaktívny účet je pozastavený)',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
