from django import forms

from django.forms import Form

class FilterResults(forms.Form):

    choice= (
        ('SML-R', 'Small Residential Buildings', ),
        ('MSM-R', 'Medium-Small Residential Buildings'),
        ('MLG-R', 'Medium Residential Buildings'),
        ('LRG-R', 'Large Residential Buildings'),
        ('XLG-R', 'Extra Large Residential Buildings'),
        ('SML-NR', 'Small NON-Residential Buildings'),
        ('MSM-NR', 'Medium NON-Residential Buildings'),
        ('MLG-NR', 'Large NON-Residential Buildings'),
        ('LRG-NR', 'Large NON-Residential Buildings'),
        ('XLG-NR','Extra NON-Large Residential Buildings')
    )

    Filter = forms.MultipleChoiceField(choices=choice)