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
            'assigned_to',
            'date_received',
            'resolution_date',
            'approved_by',
            'approval_date',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'date_received': forms.DateInput(attrs={'type': 'date'}),
            'resolution_date': forms.DateInput(attrs={'type': 'date'}),
            'approval_date': forms.DateInput(attrs={'type': 'date'}),
            'fault_description': forms.Textarea(attrs={'rows': 4}),
            'actions_taken': forms.Textarea(attrs={'rows': 4}),
            'additional_comments': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            classes = ['input-control']
            if isinstance(field.widget, forms.Textarea):
                classes.append('input-textarea')
            field.widget.attrs['class'] = ' '.join(classes)
