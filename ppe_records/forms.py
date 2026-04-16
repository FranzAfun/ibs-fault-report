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
		fields = ['ppe_type', 'date_issued']
		widgets = {
			'ppe_type': forms.TextInput(attrs={'class': 'input-control'}),
			'date_issued': forms.DateInput(attrs={'type': 'date', 'class': 'input-control'}),
		}


PPEItemFormSet = inlineformset_factory(
	PPEIssueRecord,
	PPEItem,
	form=PPEItemForm,
	extra=1,
	can_delete=True,
)
