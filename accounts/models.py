from django import forms

from contacts.models import Contact

# from django.db import models


class FormContact(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ('is_publish', 'created_date', 'author')
