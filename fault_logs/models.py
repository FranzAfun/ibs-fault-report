from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


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
