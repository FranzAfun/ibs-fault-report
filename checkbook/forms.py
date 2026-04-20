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
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'input-control'

            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs['class'] += ' input-textarea'