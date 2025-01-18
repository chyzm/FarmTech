from django import forms 
from .models import User, vendor

class vendorform(forms.ModelForm):
  #  password = forms.CharField(widget=forms.PasswordInput())
  #  confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = vendor
        fields = ['vendor_name', 'vendor_license']
    
    
   # def clean(self):
   #    cleaned_data = super(vendorform, self).clean()
   #     password = cleaned_data.get('password')
   #    confirm_password = cleaned_data.get('confirm_password')
   #     
   #     if password != confirm_password:
   #         raise forms.ValidationError(
   #             'Password does not match!'
   #         )