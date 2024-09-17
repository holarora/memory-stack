from django import forms
from .models import Entry

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = "__all__"

    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )