from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View

from .forms import PPEIssueRecordForm, PPEItemFormSet
from .models import PPEIssueRecord


class PPEIssueCreateView(View):
	template_name = 'ppe_records/ppe_form.html'

	def get(self, request):
		form = PPEIssueRecordForm()
		formset = PPEItemFormSet()

		return render(request, self.template_name, {
			'form': form,
			'formset': formset
		})

	def post(self, request):
		form = PPEIssueRecordForm(request.POST)
		formset = PPEItemFormSet(request.POST)

		if form.is_valid() and formset.is_valid():
			record = form.save()

			items = formset.save(commit=False)
			for item in items:
				item.ppe_record = record
				item.save()

			messages.success(request, 'PPE issue record created successfully.')
			return redirect('ppe_records:ppe-create')

		return render(request, self.template_name, {
			'form': form,
			'formset': formset
		})
