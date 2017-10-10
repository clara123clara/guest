from django import forms


class AddFrom(forms.Form):
    consumer_name = forms.CharField()
    consumer_type = forms.CharField()
    pl_version = forms.CharField()
    pl_url = forms.CharField()
    adminname = forms.CharField()
    adminpassword = forms.CharField()
    pl_app = forms.CharField()
    consumerContact = forms.CharField()
    consumerRemark = forms.CharField()