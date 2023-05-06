from django import forms

class UmpireMatchScoreForm(forms.Form):
    score = forms.IntegerField(
        min_value=1,
        max_value=200,
        widget=forms.NumberInput(
            attrs={'id': 'score',})
    )

class PartnerAtletForm(forms.Form):
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