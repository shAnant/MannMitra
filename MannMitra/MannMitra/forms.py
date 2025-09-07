from django import forms
from .models import UserProfile

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_pass = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = UserProfile
        fields = ["fullname","username","email","password"]
        
    def clean(self):
        cleaned_data =  super().clean()
        password = cleaned_data.get("password")
        confirm_pass = cleaned_data.get('confirm_pass')
        
        if password != confirm_pass:
            raise forms.ValidationError("Password does't match")
        

    