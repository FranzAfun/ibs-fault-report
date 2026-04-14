from django.db import models


class PPEIssueRecord(models.Model):
	employee_name = models.CharField(max_length=150)
	project = models.CharField(max_length=150, blank=True)
	job_title = models.CharField(max_length=150)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.employee_name} - {self.job_title}"


class PPEItem(models.Model):
	ppe_record = models.ForeignKey(
		PPEIssueRecord,
		on_delete=models.CASCADE,
		related_name='items'
	)
	ppe_type = models.CharField(max_length=150)
	date_issued = models.DateField()
	employee_signature = models.CharField(max_length=150, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.ppe_type} ({self.date_issued})"
