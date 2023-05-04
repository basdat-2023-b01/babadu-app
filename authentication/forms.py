from django import forms
from django.contrib.auth.forms import UserCreationForm


class LoginForm(UserCreationForm):
    nama = forms.CharField(
        label='nama',
        min_length=5,
        max_length=150,
        widget=forms.TextInput(
            attrs={'id': 'login-nama', 'placeholder': 'Nama'})
    )
    email = forms.CharField(label='email', widget=forms.TextInput(
        attrs={'id': 'login-email', 'placeholder': 'Email'}))


class RegisterAtletForm(UserCreationForm):
    PLAY_CHOICES = [
        ('1', 'Left'),
        ('2', 'Right'),
    ]
    KELAMIN_CHOICES = [
        ('1', 'Laki-laki'),
        ('2', 'Perempuan'),
    ]
    nama = forms.CharField(
        label='nama',
        min_length=5,
        max_length=150,
        widget=forms.TextInput(
            attrs={'id': 'register-atlet-nama', 'placeholder': 'Nama'})
    )
    email = forms.CharField(label='email', widget=forms.TextInput(
        attrs={'id': 'register-atlet-email', 'placeholder': 'Email'}))
    negara = forms.CharField(
        label='negara',
        min_length=5,
        max_length=25,
        widget=forms.TextInput(
            attrs={'id': 'register-atlet-negara', 'placeholder': 'Negara'})
    )
    play = forms.CharField(
        label='play',
        widget=forms.RadioSelect(
            choices=PLAY_CHOICES
        )
    )
    tinggi_badan = forms.IntegerField(
        min_value=1,
        max_value=200,
        widget=forms.NumberInput(
            attrs={'id': 'register-atlet-tinggi-badan', 'placeholder': 'Tinggi badam'})
    )
    jenis_kelamin = forms.CharField(
        label='jenis kelamin',
        widget=forms.RadioSelect(
            choices=KELAMIN_CHOICES
        )
    )


class RegisterPelatihForm(UserCreationForm):
    KATEGORI_CHOICES = [
        ('tunggal putra', 'tunggal putra'),
        ('tunggal putri', 'tunggal putri'),
        ('ganda putra', 'ganda putra'),
        ('ganda putri', 'ganda putri'),
        ('ganda campuran', 'ganda campuran'),
    ]
    nama = forms.CharField(
        label='nama',
        min_length=5,
        max_length=150,
        widget=forms.TextInput(
            attrs={'id': 'register-pelatih-nama', 'placeholder': 'Nama'})
    )
    email = forms.CharField(label='email', widget=forms.TextInput(
        attrs={'id': 'register-pelatih-email', 'placeholder': 'Email'}))
    negara = forms.CharField(
        label='negara',
        min_length=5,
        max_length=25,
        widget=forms.TextInput(
            attrs={'id': 'register-pelatih-negara', 'placeholder': 'Negara'})
    )
    kategori = forms.MultipleChoiceField(
        label='register-pelatih-kategori',
        widget=forms.CheckboxSelectMultiple,
        choices=KATEGORI_CHOICES)
    tanggal_mulai = forms.DateField(
        label='register-pelatih-tanggal-mulai',
        widget=forms.DateInput(attrs={'type': 'datetime-local'})
    )

class RegisterUmpireForm(UserCreationForm):
    nama = forms.CharField(
        label='nama',
        min_length=5,
        max_length=150,
        widget=forms.TextInput(
            attrs={'id': 'register-umpire-nama', 'placeholder': 'Nama'})
    )
    email = forms.CharField(label='email', widget=forms.TextInput(
        attrs={'id': 'register-umpire-email', 'placeholder': 'Email'}))
    negara = forms.CharField(
        label='negara',
        min_length=5,
        max_length=25,
        widget=forms.TextInput(
            attrs={'id': 'register-umpire-negara', 'placeholder': 'Negara'})
    )