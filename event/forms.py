from django import forms

class UmpireMatchScoreForm(forms.Form):
    score = forms.IntegerField(
        min_value=1,
        max_value=200,
        widget=forms.NumberInput(
            attrs={'id': 'score',})
    )

class GandaPartnerForm(forms.Form):
    def __init__(self, atlet, *args, **kwargs):
        super(GandaPartnerForm, self).__init__(*args, **kwargs)
        self.fields['daftar_atlet'].choices = atlet
        self.fields['daftar_atlet'].widget.attrs.update({'class': 'w-60 px-4 py-2 border border-shark-400 bg-transparent outline-none focus:border-primary-400 rounded-md transition text-white'})
    
    def is_valid(self):
        valid = super().is_valid()
        
        if not self.cleaned_data.get('daftar_atlet'):
            self.add_error('daftar_atlet', 'Daftar atlet harus diisi')
            return False
        return valid

    daftar_atlet = forms.ChoiceField()

class TunggalForm(forms.Form):
    pass

class UnenrollEventForm(forms.Form):
    pass
