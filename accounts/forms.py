from django import forms
from .models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email','password']
        
    widgets = {
        'first_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring focus:border-blue-500'}),
        'last_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring focus:border-blue-500'}),
        'username': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring focus:border-blue-500'}),
        'email': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring focus:border-blue-500'}),
    }
        