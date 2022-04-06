from django import forms

my_file = open('dono.txt', 'r')
dono = my_file.read().split('\n')

CHOICES= [
    ('0', str(dono[0])),
    ('1', str(dono[1])),
    ('2', str(dono[2])),
    ('3', str(dono[3])),
    ('4', str(dono[4])),
]

class DonationForm(forms.Form):
    dono_options= forms.IntegerField(label='', widget=forms.RadioSelect(choices=CHOICES))

class MyCustomForm(forms.Form):
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('my_choices')
        super(MyCustomForm, self).__init__(*args, **kwargs)
        self.fields["my_field"] = forms.ChoiceField(choices=choices, widget=forms.RadioSelect, label='')
