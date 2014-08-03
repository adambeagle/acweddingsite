from email.mime.text import MIMEText
from os import environ
import smtplib

from django import forms
from django.conf import settings
from django.core.mail import send_mail

class ContactForm(forms.Form):
    """
    Basic "contact us" form. On is_valid, sends email using form data to owner.
    """
    name = forms.CharField(max_length=64, label='Your name')
    email_address = forms.EmailField(label='Your email address')
    cc_sender = forms.BooleanField(required=False, label='Send copy of message to email address above')
    message = forms.CharField(widget=forms.Textarea(
        attrs={
            'rows' : '10',
            'class' : 'form-control',
        })
    )
    
    error_css_class = 'form-error'
    
    def send_email(self):
        """
        Sends email to owner based on form data.
        Uses django.core.mail's send_email, which uses EMAIL_HOST_* (etc.) settings.
        Assumes existence of DOMAIN and CONTACT_EMAIL environment variables.
        Expects self.cleaned_data to be populated, so must be called after is_valid().
        """
        cleaned = self.cleaned_data
        domain = str(environ['DOMAIN'])
        sbj = '[{0}] Message from {1} at {2}'.format(
            domain, 
            cleaned['name'],
            cleaned['email_address']
        )
        msg = cleaned['message']
        fromaddr = 'info@{0}'.format(domain)
        recipients = [environ['CONTACT_EMAIL']]
        
        # Send to site owner
        send_mail(sbj, msg, fromaddr, recipients)
        
        # Send copy to user, if requested
        if cleaned['cc_sender']:
            sbj = 'Your message to {0}'.format(domain)
            recipients = [cleaned['email_address']]
            send_mail(sbj, msg, fromaddr, recipients)
