from django import forms
from django.forms import inlineformset_factory

from .models import AssetItem, AssetRecord


class AssetRecordForm(forms.ModelForm):
    class Meta:
        model = AssetRecord
        fields = ['employee_name', 'project', 'job_title', 'approved_by', 'approval_date']
        widgets = {
            'approval_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                if isinstance(field.widget, forms.Select):
                    field.widget.attrs['class'] = 'form-select'
                else:
                    field.widget.attrs['class'] = 'form-control'


class AssetItemForm(forms.ModelForm):
    class Meta:
        model = AssetItem
        fields = ['asset_type', 'date_issued', 'issued_by']
        widgets = {
            'date_issued': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                if isinstance(field.widget, forms.Select):
                    field.widget.attrs['class'] = 'form-select'
                else:
                    field.widget.attrs['class'] = 'form-control'


AssetItemFormSet = inlineformset_factory(
    AssetRecord,
    AssetItem,
    form=AssetItemForm,
    extra=1,
    can_delete=True,
)
