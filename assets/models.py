from django.db import models
from django.utils import timezone


class AssetRecord(models.Model):
	reference_number = models.CharField(max_length=64, unique=True, db_index=True, blank=True)
	employee_name = models.CharField(max_length=150)
	project = models.CharField(max_length=150)
	job_title = models.CharField(max_length=150)
	approved_by = models.CharField(max_length=150, blank=True)
	approval_date = models.DateField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at', '-id']

	@classmethod
	def _next_reference(cls, reference_date) -> str:
		prefix = f'AR-{reference_date.strftime("%Y%m%d")}'
		count = cls.objects.filter(reference_number__startswith=prefix).count()
		return f'{prefix}-{count + 1:04d}'

	def save(self, *args, **kwargs):
		if not self.reference_number:
			self.reference_number = self._next_reference(timezone.localdate())
		super().save(*args, **kwargs)

	def __str__(self) -> str:
		return f'{self.reference_number} - {self.employee_name}'


class AssetItem(models.Model):
	asset_record = models.ForeignKey(
		AssetRecord,
		on_delete=models.CASCADE,
		related_name='items',
	)
	asset_type = models.CharField(max_length=150)
	date_issued = models.DateField()
	issued_by = models.CharField(max_length=150)
	employee_signature = models.CharField(max_length=150, blank=True)

	def __str__(self) -> str:
		return f'{self.asset_type} ({self.date_issued})'
