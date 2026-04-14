from pathlib import Path

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import Q
from django.utils import timezone


ALLOWED_ATTACHMENT_EXTENSIONS = [
    'pdf',
    'png',
    'jpg',
    'jpeg',
    'gif',
    'webp',
    'bmp',
    'txt',
    'csv',
    'doc',
    'docx',
    'xls',
    'xlsx',
]
MAX_ATTACHMENT_SIZE = 10 * 1024 * 1024  # 10 MB per file
MAX_ATTACHMENTS_PER_REPORT = 10


def fault_report_attachment_upload_to(instance: 'FaultReportAttachment', filename: str) -> str:
    safe_name = Path(filename).name.replace(' ', '_')
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    return f'fault_reports/{instance.fault_report.reference_number}/{timestamp}_{safe_name}'


class FaultReport(models.Model):
    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        RESOLVED = 'RESOLVED', 'Resolved'
        CLOSED = 'CLOSED', 'Closed'

    reference_number = models.CharField(max_length=64, unique=True, db_index=True)
    report_date = models.DateField(db_index=True)
    report_time = models.TimeField()
    reporter_name = models.CharField(max_length=150)
    role = models.CharField(max_length=100)
    reporter_contact = models.CharField(max_length=150)
    location = models.CharField(max_length=255)
    complaint_summary = models.TextField()
    investigation_findings = models.TextField(blank=True)
    resolution = models.TextField(blank=True)
    action_taken_by = models.CharField(max_length=150, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN,
        db_index=True,
    )
    date_of_resolution = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-report_date', '-report_time', '-id']
        constraints = [
            models.CheckConstraint(
                name='faultreport_resolution_date_consistency',
                condition=(
                    Q(status__in=['OPEN', 'IN_PROGRESS'], date_of_resolution__isnull=True)
                    | Q(status__in=['RESOLVED', 'CLOSED'], date_of_resolution__isnull=False)
                ),
            )
        ]
        indexes = [
            models.Index(fields=['status', 'report_date']),
        ]

    def clean(self) -> None:
        resolved_statuses = {self.Status.RESOLVED, self.Status.CLOSED}
        if self.status in resolved_statuses and not self.date_of_resolution:
            raise ValidationError(
                {'date_of_resolution': 'Date of resolution is required for resolved or closed reports.'}
            )

        if self.status not in resolved_statuses and self.date_of_resolution:
            raise ValidationError(
                {'date_of_resolution': 'Date of resolution must be empty unless status is resolved or closed.'}
            )

        if self.date_of_resolution and self.report_date and self.date_of_resolution < self.report_date:
            raise ValidationError(
                {'date_of_resolution': 'Date of resolution cannot be earlier than report date.'}
            )

    def __str__(self) -> str:
        return f'{self.reference_number} ({self.get_status_display()})'


class FaultReportAttachment(models.Model):
    fault_report = models.ForeignKey(
        FaultReport,
        on_delete=models.CASCADE,
        related_name='attachments',
    )
    file = models.FileField(
        upload_to=fault_report_attachment_upload_to,
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_ATTACHMENT_EXTENSIONS)],
    )
    original_name = models.CharField(max_length=255, blank=True)
    file_size = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['fault_report', '-uploaded_at']),
        ]

    def clean(self) -> None:
        if self.file and self.file.size > MAX_ATTACHMENT_SIZE:
            raise ValidationError({'file': 'Each file must be 10 MB or smaller.'})

    def save(self, *args, **kwargs):
        if self.file:
            if not self.original_name:
                self.original_name = Path(self.file.name).name
            self.file_size = self.file.size
        super().save(*args, **kwargs)

    @property
    def filename(self) -> str:
        return self.original_name or Path(self.file.name).name

    @property
    def extension(self) -> str:
        return Path(self.filename).suffix.lower().lstrip('.')

    @property
    def is_image(self) -> bool:
        return self.extension in {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'}

    @property
    def is_pdf(self) -> bool:
        return self.extension == 'pdf'

    @property
    def file_size_display(self) -> str:
        if self.file_size >= 1024 * 1024:
            return f'{self.file_size / (1024 * 1024):.1f} MB'
        if self.file_size >= 1024:
            return f'{self.file_size / 1024:.1f} KB'
        return f'{self.file_size} B'

    def __str__(self) -> str:
        return f'{self.fault_report.reference_number} - {self.filename}'
