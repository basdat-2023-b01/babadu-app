from django import forms

class DaftarAtletForm(forms.Form):
    def __init__(self, atlet, *args, **kwargs):
        super(DaftarAtletForm, self).__init__(*args, **kwargs)
        self.fields['daftar_atlet'].choices = atlet
    
    def is_valid(self):
        valid = super().is_valid()
        
        if not self.cleaned_data.get('daftar_atlet'):
            self.add_error('daftar_atlet', 'Daftar atlet harus diisi')
            return False
        return valid

    daftar_atlet = forms.ChoiceField()
