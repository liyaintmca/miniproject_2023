from django import forms
from .models import Docs,Deps

class DoctorForm(forms.Form):
    model=Docs
    Name = forms.CharField(label='First Name', max_length=100)
    email = forms.EmailField(label='Email')
    dob = forms.DateField(label='Date of Birth', widget=forms.DateInput(attrs={'class': 'datetimepicker'}))
    address = forms.CharField(label='Address', widget=forms.Textarea)
    city = forms.CharField(label='City', max_length=100)
    postal_code = forms.CharField(label='Postal Code', max_length=10)
    phone = forms.CharField(label='Phone', max_length=20)
 
 
class DepartmentForm(forms.ModelForm):
    model=Deps
    DepName=forms.CharField(label='Department Name',max_length=100)
    DepDesc=forms.CharField(label='Department Description',max_length=100)
#     class Meta:
#         model = Department
#         fields = ('name', 'description', 'location')  # Add other fields as needed

# class DoctorForm(forms.ModelForm):
#     class Meta:
#         model = Doctor
#         fields = ('first_name', 'last_name', 'email', 'date_of_birth', 'address', 'city', 'postal', 'phone')  # Add other fields as needed
