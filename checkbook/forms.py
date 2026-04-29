from django import forms

from .models import CheckbookEntry


class CheckbookEntryForm(forms.ModelForm):
    class Meta:
        model = CheckbookEntry
        fields = [
            'date',
            'ref_code',
            'num',
            'description',
            'category',
            'withdrawal_amount',
            'deposit_amount',
            'balance',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                if isinstance(field.widget, forms.Select):
                    field.widget.attrs['class'] = 'form-select'
                else:
                    field.widget.attrs['class'] = 'form-control'
