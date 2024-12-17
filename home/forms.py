from django import forms
from . import models

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)

# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Submit
# serial_no
# type
# title
# status
class MyForm(forms.Form):
    my_field = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'border border-gray-300 rounded-md'
    }))
class Airport(forms.ModelForm):
    class Meta:
        model = models.Airport
        fields = "__all__"
        # exclude = ['created_by']

class EqptForm(forms.ModelForm):
    class Meta:
        model = models.Equipment
        fields = "__all__"
        widgets = {
            "__all__": forms.TextInput(attrs={
                'class': 'border border-gray-300 rounded-md'
            }),
        }
        # fields = ['serial_no', 'type', 'title', 'status']
class StaffForm(forms.ModelForm):
    class Meta:
        model = models.Staff
        fields = "__all__"
        exclude = ['created_by',]
class RepairForm(forms.ModelForm):
   
    class Meta:
        model = models.Repair
        fields = "__all__"
    
class PlaceInstallationForm(forms.ModelForm):
    class Meta:
        model = models.PlaceInstallaion
        fields = "__all__"
class EqptTypesForm(forms.ModelForm):
    class Meta:
        model = models.EqptType
        fields = "__all__"
class EqptStatusForm(forms.ModelForm):
    class Meta:
        model = models.EqptStatus
        fields = "__all__"

