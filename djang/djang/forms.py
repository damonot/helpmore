from tkinter import HIDDEN
from django import forms

class RadioForm(forms.Form):
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('my_choices')
        super(RadioForm, self).__init__(*args, **kwargs)
        self.fields["my_field"] = forms.ChoiceField(choices=choices, widget=forms.RadioSelect, label='')

class DropdownForm(forms.Form):
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('my_choices')
        super(DropdownForm, self).__init__(*args, **kwargs)
        self.fields["my_tip"] = forms.ChoiceField(choices=choices, widget=forms.Select, label='')

class InputForm(forms.Form):
    my_input = forms.IntegerField(required=False,label='')


