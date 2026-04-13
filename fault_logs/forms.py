from django import forms

from .models import FaultReport


class FaultReportForm(forms.ModelForm):
    class Meta:
        model = FaultReport
        fields = [
            'reference_number',
            'report_date',
            'report_time',
            'reporter_name',
            'role',
            'reporter_contact',
            'location',
            'complaint_summary',
            'investigation_findings',
            'resolution',
            'action_taken_by',
            'status',
            'date_of_resolution',
        ]
        labels = {
            'reference_number': 'Reference Number',
            'report_date': 'Report Date',
            'report_time': 'Report Time',
            'reporter_name': 'Reporter Name',
            'role': 'Role',
            'reporter_contact': 'Reporter Contact',
            'location': 'Location',
            'complaint_summary': 'Complaint Summary',
            'investigation_findings': 'Investigation & Findings',
            'resolution': 'Resolution',
            'action_taken_by': 'Action Taken By',
            'status': 'Status',
            'date_of_resolution': 'Date of Resolution',
        }
        widgets = {
            'report_date': forms.DateInput(attrs={'type': 'date'}),
            'report_time': forms.TimeInput(attrs={'type': 'time'}),
            'date_of_resolution': forms.DateInput(attrs={'type': 'date'}),
            'complaint_summary': forms.Textarea(attrs={'rows': 4}),
            'investigation_findings': forms.Textarea(attrs={'rows': 4}),
            'resolution': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            classes = ['input-control']
            if isinstance(field.widget, forms.Textarea):
                classes.append('input-textarea')
            field.widget.attrs['class'] = ' '.join(classes)

            if field_name == 'status':
                field.widget.attrs['class'] = f"{field.widget.attrs['class']} input-select"
