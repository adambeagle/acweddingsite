from email.mime.text import MIMEText
import smtplib

from django import forms


class ContactForm(forms.Form):
    error_css_class = 'form-error'
    required_css_class = 'form-required'
    name = forms.CharField(max_length=64)
    email_address = forms.EmailField()
    cc_sender = forms.BooleanField(required=False, label='Send copy of message to email address above')
    message = forms.CharField(widget=forms.Textarea)
    
    def send_email(self):
        """
        Sends email to user based on environment variables. 
        Expects self.cleaned_data to be populated, so must be called after is_valid().
        """
        print('send email')
        
        
        
    
    