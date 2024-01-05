from django import forms
from django.forms import ModelForm
from .models import tarea


class tareaForm(forms.ModelForm):
    class Meta:
        model = tarea
        fields = ["title","description","important"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "important": forms.CheckboxInput(attrs={"class": "form-check-input m-auto"})
        }
