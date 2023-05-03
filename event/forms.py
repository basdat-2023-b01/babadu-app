from django import forms

class UmpireMatchScoreForm(forms.Form):
    score = forms.IntegerField(
        min_value=1,
        max_value=200,
        widget=forms.NumberInput(
            attrs={'id': 'score',})
    )