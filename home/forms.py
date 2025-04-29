from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Your Email'}))
    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Subject'}))
    phone = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'placeholder': 'Your Phone Number (Optional)'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Your Message', 'rows': 5, 'cols': 40}))


class DirectContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Your Email'}))
    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Subject'}))
    phone = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'placeholder': 'Your Phone Number (Optional)'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Your Message', 'rows': 5, 'cols': 40}))