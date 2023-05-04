from django import forms

class DaftarAtletForm(forms.Form):
    ATLET = [
        ('1', 'Gregoria Mariska Tunjung'),
        ('2', 'Putri Kusuma Wardani'),
        ('3', 'Greysia Polii'),
        ('4', 'Apriyani Rahayu'),
        ('5', 'Anthony Sinisuka Ginting'),
        ('6', 'Jonatan Christie'),
        ('7', 'Kevin Sanjaya Sukamuljo'),
        ('8', 'Marcus Fernaldi Gideon'),
        ('9', 'Fajar Alfian'),
        ('10', 'Muhammad Rian Ardianto'),
    ]
    daftar_atlet = forms.CharField(
        label='daftar atlet',
        widget=forms.Select(
            choices=ATLET
        )
    )