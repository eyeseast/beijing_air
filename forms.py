import datetime
from django import forms
from django.contrib.admin.widgets import AdminDateWidget

class DateRangeForm(forms.Form):
    start = forms.DateField(widget=AdminDateWidget, required=False)
    end = forms.DateField(widget=AdminDateWidget, required=False)