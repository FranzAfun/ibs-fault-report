from django import forms

from .models import AssetFaultReport


class AssetFaultReportForm(forms.ModelForm):
    class Meta:
        model = AssetFaultReport
        fields = [
            'date',
            'employee_name',
            'job_title',
            'asset_type',
            'asset_serial_number',
            'fault_description',
            'severity',
            'actions_taken',
            'additional_comments',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fault_description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'actions_taken': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'additional_comments': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                if isinstance(field.widget, forms.Select):
                    field.widget.attrs['class'] = 'form-select'
                else:
                    field.widget.attrs['class'] = 'form-control'


class AssetFaultAssignForm(forms.ModelForm):
    class Meta:
        model = AssetFaultReport
        fields = ['assigned_to', 'date_received']
        widgets = {
            'date_received': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                if isinstance(field.widget, forms.Select):
                    field.widget.attrs['class'] = 'form-select'
                else:
                    field.widget.attrs['class'] = 'form-control'


class AssetFaultResolveForm(forms.ModelForm):
    class Meta:
        model = AssetFaultReport
        fields = ['resolution_date', 'resolution_description']
        widgets = {
            'resolution_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'resolution_description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                if isinstance(field.widget, forms.Select):
                    field.widget.attrs['class'] = 'form-select'
                else:
                    field.widget.attrs['class'] = 'form-control'
