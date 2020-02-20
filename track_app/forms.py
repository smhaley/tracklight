from django import forms


class HomeForm(forms.Form):
    url_post = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': "form-control",
            'type': "text",
            'name': "url_post",
            'placeholder': "Enter URL to Scan",
            'maxlength': "100",
            'required': 'required'
        }
    ))
    delay = forms.ChoiceField(choices=[(i, i) for i in range(1, 11)],
                              required=False,
                              initial=4, widget=forms.Select(
            {
                'class': 'btn btn-secondary dropdown-toggle btn-sm'
            }
        ))


class ContactForm(forms.Form):
    # bootstrap is handling email style verification
    sender = forms.CharField(required=False,
                             widget=forms.TextInput(
                                attrs={
                                    'type': "email",
                                    'class': "form-control",
                                    'name': "sender",
                                    'placeholder': "name@example.com"
                                }
                             ))
    message = forms.CharField(widget=forms.Textarea(
        {
            'class': "form-control",
            'name': "message",
            'rows': "4",
            'required': 'required'
        }
    ))


