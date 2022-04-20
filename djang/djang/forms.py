from tkinter import HIDDEN
from django import forms

class RadioForm(forms.Form):
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('my_choices')
        super(RadioForm, self).__init__(*args, **kwargs)
        self.fields["my_radio"] = forms.ChoiceField(choices=choices, widget=forms.RadioSelect, label='')

class DropdownForm(forms.Form):
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('my_choices')
        super(DropdownForm, self).__init__(*args, **kwargs)
        self.fields["my_tip"] = forms.ChoiceField(choices=choices, widget=forms.Select, label='')

class InputForm(forms.Form):
    my_input = forms.FloatField(required=False,label='', min_value=0,
                            error_messages={'min_value': u'Price cannot be less than 0.00'})
    


