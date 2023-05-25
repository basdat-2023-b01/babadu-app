from django import forms

class DaftarSponsorForm(forms.Form):
    def __init__(self, sponsor, *args, **kwargs):
        super(DaftarSponsorForm, self).__init__(*args, **kwargs)
        self.fields['daftar_sponsor'].choices = sponsor
    
    def is_valid(self):
        valid = super().is_valid()
        
        if not self.cleaned_data.get('daftar_sponsor'):
            self.add_error('daftar_sponsor', 'Sponsor harus diisi')
            return False
        return valid

    daftar_sponsor = forms.ChoiceField()
    tgl_mulai = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    tgl_selesai = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))