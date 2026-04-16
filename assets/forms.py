from django import forms
from django.forms import inlineformset_factory

from .models import AssetItem, AssetRecord


class AssetRecordForm(forms.ModelForm):
	class Meta:
		model = AssetRecord
		fields = ['employee_name', 'project', 'job_title', 'approved_by', 'approval_date']
		widgets = {
			'approval_date': forms.DateInput(attrs={'type': 'date'}),
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		for field_name, field in self.fields.items():
			classes = ['input-control']
			if isinstance(field.widget, forms.Textarea):
				classes.append('input-textarea')
			field.widget.attrs['class'] = ' '.join(classes)


class AssetItemForm(forms.ModelForm):
	class Meta:
		model = AssetItem
		fields = ['asset_type', 'date_issued', 'issued_by', 'employee_signature']
		widgets = {
			'date_issued': forms.DateInput(attrs={'type': 'date'}),
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		for field_name, field in self.fields.items():
			classes = ['input-control']
			if isinstance(field.widget, forms.Textarea):
				classes.append('input-textarea')
			field.widget.attrs['class'] = ' '.join(classes)


AssetItemFormSet = inlineformset_factory(
	AssetRecord,
	AssetItem,
	form=AssetItemForm,
	extra=1,
	can_delete=True,
)
