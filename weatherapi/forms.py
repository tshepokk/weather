from django import forms
from django.shortcuts import render


class WeatherForm(forms.Form):
    city_name = forms.CharField(label='City Name', max_length=10),
    period = forms.IntegerField(min_value=1, max_value=7),
