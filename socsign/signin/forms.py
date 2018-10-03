from django import forms

from .models import EventForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout


class EventFormBase(forms.Form):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    mobile_number = forms.CharField()
    home_phone_number = forms.CharField()
    address = forms.CharField()
    city = forms.CharField()
    zip_code = forms.CharField()

    interest = forms.MultipleChoiceField(
        required=False,
        label='-',
        widget=forms.CheckboxSelectMultiple,
        choices=[],
    )


    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'

        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-default'))

        self.fields['interest'].choices = [
            (choice.tag, choice.caption) for choice in
            event.interest_choices.all()
        ]


class EventFormStandard(EventFormBase):
    pass


class EventFormLabor(EventFormBase):
    pass




