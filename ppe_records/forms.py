from django import forms
from django.forms import inlineformset_factory

from .models import PPEIssueRecord, PPEItem


class PPEIssueRecordForm(forms.ModelForm):
	class Meta:
		model = PPEIssueRecord
		fields = ['employee_name', 'project', 'job_title']
		widgets = {
			'employee_name': forms.TextInput(attrs={'class': 'input-control'}),
			'project': forms.TextInput(attrs={'class': 'input-control'}),
			'job_title': forms.TextInput(attrs={'class': 'input-control'}),
		}


class PPEItemForm(forms.ModelForm):
	class Meta:
		model = PPEItem
		fields = ['ppe_type', 'date_issued', 'employee_signature']
		widgets = {
			'ppe_type': forms.TextInput(attrs={'class': 'input-control'}),
			'date_issued': forms.DateInput(attrs={'type': 'date', 'class': 'input-control'}),
			'employee_signature': forms.CheckboxInput(attrs={'class': 'checkbox-control'}),
		}

	def clean_employee_signature(self):
		value = self.cleaned_data.get('employee_signature')
		if value in (True, 'on', 'true', 'True', '1', 1):
			return 'Signed'
		return ''


PPEItemFormSet = inlineformset_factory(
	PPEIssueRecord,
	PPEItem,
	form=PPEItemForm,
	extra=1,
	can_delete=True,
)
