from pathlib import Path

from django import forms

from .models import (
    ALLOWED_ATTACHMENT_EXTENSIONS,
    MAX_ATTACHMENTS_PER_REPORT,
    MAX_ATTACHMENT_SIZE,
    FaultReport,
)


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        if not data:
            if self.required:
                raise forms.ValidationError(self.error_messages['required'], code='required')
            return []

        if not isinstance(data, (list, tuple)):
            data = [data]

        cleaned = []
        errors = []

        for uploaded in data:
            try:
                cleaned.append(super().clean(uploaded, initial))
            except forms.ValidationError as exc:
                errors.extend(exc.error_list)

        if errors:
            raise forms.ValidationError(errors)

        return cleaned


class FaultReportForm(forms.ModelForm):
    attachments = MultipleFileField(
        required=False,
        help_text='Upload PDF, images, and standard office files (up to 10 files, 10 MB each).',
    )

    class Meta:
        model = FaultReport
        fields = [
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

        self.fields['attachments'].widget.attrs.update(
            {
                'class': 'input-control',
                'multiple': True,
                'accept': '.pdf,.png,.jpg,.jpeg,.gif,.webp,.bmp,.txt,.csv,.doc,.docx,.xls,.xlsx',
            }
        )

    def clean_attachments(self):
        uploads = self.cleaned_data.get('attachments') or []
        if not uploads:
            return []

        existing_count = 0
        if self.instance and self.instance.pk:
            existing_count = self.instance.attachments.count()

        if len(uploads) > MAX_ATTACHMENTS_PER_REPORT:
            raise forms.ValidationError(
                f'You can upload up to {MAX_ATTACHMENTS_PER_REPORT} files at a time.'
            )

        if existing_count + len(uploads) > MAX_ATTACHMENTS_PER_REPORT:
            allowed_now = MAX_ATTACHMENTS_PER_REPORT - existing_count
            raise forms.ValidationError(
                f'This report already has {existing_count} file(s). You can add only {allowed_now} more.'
            )

        errors = []
        allowed = set(ALLOWED_ATTACHMENT_EXTENSIONS)

        for upload in uploads:
            extension = Path(upload.name).suffix.lower().lstrip('.')
            if extension not in allowed:
                errors.append(
                    f'{upload.name}: unsupported file type. Allowed: {", ".join(sorted(allowed))}.'
                )
            if upload.size > MAX_ATTACHMENT_SIZE:
                errors.append(
                    f'{upload.name}: exceeds maximum size of {MAX_ATTACHMENT_SIZE // (1024 * 1024)} MB.'
                )

        if errors:
            raise forms.ValidationError(errors)

        return uploads
