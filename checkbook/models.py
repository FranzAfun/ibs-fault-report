from django.db import models
from django.utils import timezone


class CheckbookEntry(models.Model):
	reference_number = models.CharField(max_length=64, unique=True, db_index=True, blank=True)

	date = models.DateField()
	ref_code = models.CharField(max_length=50, blank=True)
	num = models.CharField(max_length=50, blank=True)

	description = models.TextField()
	category = models.CharField(max_length=150, blank=True)

	withdrawal_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	deposit_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

	balance = models.DecimalField(max_digits=12, decimal_places=2)

	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-date', '-id']

	@classmethod
	def _next_reference(cls, reference_date) -> str:
		prefix = f'CB-{reference_date.strftime("%Y%m%d")}'
		count = cls.objects.filter(reference_number__startswith=prefix).count()
		return f'{prefix}-{count + 1:04d}'

	def save(self, *args, **kwargs):
		if not self.reference_number:
			self.reference_number = self._next_reference(timezone.localdate())
		super().save(*args, **kwargs)

	def __str__(self):
		return f'{self.reference_number} - {self.description[:30]}'
