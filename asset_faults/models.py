from django.db import models
from django.utils import timezone


ASSET_TYPE_CHOICES = [
	('laptop', 'Laptop'),
	('desktop', 'Desktop Computer'),
	('monitor', 'Monitor'),
	('mobile_phone', 'Mobile Phone'),
	('tablet', 'Tablet'),
	('printer', 'Printer'),
	('keyboard', 'Keyboard'),
	('mouse', 'Mouse'),
	('usb_drive', 'USB Drive'),
	('external_hdd', 'External Hard Drive'),
	('headset', 'Headset'),
	('webcam', 'Webcam'),
	('router', 'Router / Switch'),
	('ups', 'UPS / Battery Backup'),
	('other', 'Other'),
]


class AssetFaultReport(models.Model):
	class Severity(models.TextChoices):
		LOW = 'low', 'Low'
		MEDIUM = 'medium', 'Medium'
		HIGH = 'high', 'High'

	reference_number = models.CharField(max_length=64, unique=True, db_index=True, blank=True)
	date = models.DateField(db_index=True)
	employee_name = models.CharField(max_length=150)
	job_title = models.CharField(max_length=150)
	asset_type = models.CharField(max_length=150, choices=ASSET_TYPE_CHOICES)
	asset_serial_number = models.CharField(max_length=150)
	fault_description = models.TextField()
	severity = models.CharField(max_length=10, choices=Severity.choices, default=Severity.LOW, db_index=True)
	actions_taken = models.TextField(blank=True)
	additional_comments = models.TextField(blank=True)
	assigned_to = models.CharField(max_length=150, blank=True)
	it_signature = models.BooleanField(default=False)
	date_received = models.DateField(null=True, blank=True)
	resolution_date = models.DateField(null=True, blank=True)
	resolution_description = models.TextField(blank=True)
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
