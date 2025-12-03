from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Role, LocationConstraint

class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form with additional fields"""
    
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    role = forms.ModelChoiceField(queryset=Role.objects.all(), required=True)
    
    class Meta:
        model = User
        fields = ("roll_number", "email", "first_name", "last_name", "role", "password1", "password2")
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.role = self.cleaned_data["role"]
        if commit:
            user.save()
        return user

class LocationConstraintForm(forms.ModelForm):
    """Form for creating and updating location constraints"""
    
    class Meta:
        model = LocationConstraint
        fields = ['name', 'latitude', 'longitude', 'radius', 'is_active']
        widgets = {
            'latitude': forms.NumberInput(attrs={'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'step': '0.000001'}),
            'radius': forms.NumberInput(attrs={'step': '0.01'}),
        }
    
    def clean_radius(self):
        radius = self.cleaned_data.get('radius')
        if radius <= 0:
            raise forms.ValidationError("Radius must be greater than 0.")
        return radius