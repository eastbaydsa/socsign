from django import forms

from .models import EventForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout

from localflavor.us.forms import USZipCodeField
from phonenumber_field.formfields import PhoneNumberField


class EventFormBase(forms.Form):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    mobile_number = PhoneNumberField(required=False)
    home_phone_number = PhoneNumberField(required=False)
    address = forms.CharField(required=False)
    city = forms.CharField(required=False)
    zip_code = USZipCodeField(required=False)

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
        self.helper.label_class = 'col-lg-2 offset-lg-2'
        self.helper.field_class = 'col-lg-6'

        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-default'))

        self.fields['interest'].choices = [
            (choice.tag, choice.caption) for choice in
            event.interest_choices.all()
        ]


class EventFormStandard(EventFormBase):
    pass


class EventFormLabor(EventFormBase):
    labor_member = forms.ChoiceField(
        label='Are you in a union?',
        required=False,
        choices=[('yes', 'Yes'), ('no', 'No')],
    )

    wants_labor_help = forms.ChoiceField(
        label='Do you want help organizing your workplace?',
        required=False,
        choices=[('yes', 'Yes'), ('no', 'No')],
    )

    union = forms.CharField(
        label="What's your local?",
        required=False,
    )


