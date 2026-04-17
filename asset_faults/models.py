from django.db import models
from django.utils import timezone


class AssetFaultReport(models.Model):
	class Severity(models.TextChoices):
		LOW = 'low', 'Low'
		MEDIUM = 'medium', 'Medium'
		HIGH = 'high', 'High'

	reference_number = models.CharField(max_length=64, unique=True, db_index=True, blank=True)
	date = models.DateField(db_index=True)
	employee_name = models.CharField(max_length=150)
	job_title = models.CharField(max_length=150)
	asset_type = models.CharField(max_length=150)
	asset_serial_number = models.CharField(max_length=150)
	fault_description = models.TextField()
	severity = models.CharField(max_length=10, choices=Severity.choices, default=Severity.LOW, db_index=True)
	actions_taken = models.TextField(blank=True)
	additional_comments = models.TextField(blank=True)
	employee_signed = models.BooleanField(default=False)
	employee_signed_date = models.DateField(null=True, blank=True)
	assigned_to = models.CharField(max_length=150, blank=True)
	it_signature = models.BooleanField(default=False)
	date_received = models.DateField(null=True, blank=True)
	resolution_date = models.DateField(null=True, blank=True)
	approved_by = models.CharField(max_length=150, blank=True)
	approved_signature = models.BooleanField(default=False)
	approval_date = models.DateField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at', '-id']

	@classmethod
	def _next_reference(cls, reference_date) -> str:
		prefix = f'AFR-{reference_date.strftime("%Y%m%d")}'
		count = cls.objects.filter(reference_number__startswith=prefix).count()
		return f'{prefix}-{count + 1:04d}'

	def save(self, *args, **kwargs):
		if not self.reference_number:
			reference_date = self.date or timezone.localdate()
			self.reference_number = self._next_reference(reference_date)
		super().save(*args, **kwargs)

	def __str__(self) -> str:
		return f'{self.reference_number} - {self.employee_name}'
