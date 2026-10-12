from django import forms
from .models import Taxi, Driver

class TaxiForm(forms.ModelForm):
    class Meta:
        model = Taxi
        fields = ['number', 'type', 'source', 'destination', 'price', 'availability', 'driver']
        widgets = {
            'number': forms.TextInput(attrs={
                'class': 'form-control custom-input text-uppercase',
                'placeholder': 'e.g. MH-02-AB-1234',
                'required': True,
                'autofocus': True,
            }),
            'type': forms.Select(attrs={
                'class': 'form-select custom-input',
            }),
            'source': forms.TextInput(attrs={
                'class': 'form-control custom-input',
                'placeholder': 'e.g. Domestic Airport T1, Mumbai',
                'required': True,
            }),
            'destination': forms.TextInput(attrs={
                'class': 'form-control custom-input',
                'placeholder': 'e.g. BKC Business Hub, Bandra',
                'required': True,
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control custom-input',
                'placeholder': 'e.g. 450.00',
                'step': '0.01',
                'min': '0',
                'required': True,
            }),
            'availability': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'role': 'switch',
            }),
            'driver': forms.Select(attrs={
                'class': 'form-select custom-input',
                'required': True,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['driver'].queryset = Driver.objects.all().order_by('name')
        self.fields['driver'].empty_label = "-- Select Driver --"
        if not self.instance.pk:
            self.initial['availability'] = True
