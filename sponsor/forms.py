from django import forms


class DaftarSponsorForm(forms.Form):
    SPONSOR = [
        ('1', 'Djarum'),
        ('2', 'Gudang Garam'),
        ('3', 'Sampoerna'),
        ('4', 'Wismilak'),
        ('5', 'Bentoel'),
        ('6', 'Surya'),
        ('7', 'Marlboro'),
        ('8', 'Dunhill'),
        ('9', 'Sampoerna'),
        ('10', 'Sampoerna'),
    ]
    daftar_sponsor = forms.CharField(
        label='daftar sponsor',
        widget=forms.Select(
            choices=SPONSOR
        )
    )
    date_field = forms.DateField()
    