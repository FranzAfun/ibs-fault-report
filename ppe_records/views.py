from django.contrib import messages
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import DeleteView, DetailView, ListView

from .forms import PPEIssueRecordForm, PPEItemFormSet
from .models import PPEIssueRecord


class PPEIssueListView(ListView):
	model = PPEIssueRecord
	template_name = 'ppe_records/ppe_list.html'
	context_object_name = 'records'

	def get_queryset(self):
		return PPEIssueRecord.objects.annotate(
			total_items=Count('items'),
			signed_items=Count('items', filter=~Q(items__employee_signature='')),
		).order_by('-created_at')


class PPEIssueDetailView(DetailView):
	model = PPEIssueRecord
	template_name = 'ppe_records/ppe_detail.html'
	context_object_name = 'record'

	def get_queryset(self):
		return PPEIssueRecord.objects.prefetch_related('items')


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


class PPEIssueUpdateView(View):
	template_name = 'ppe_records/ppe_form.html'

	def get(self, request, pk):
		record = PPEIssueRecord.objects.get(pk=pk)

		form = PPEIssueRecordForm(instance=record)
		formset = PPEItemFormSet(instance=record)

		return render(request, self.template_name, {
			'form': form,
			'formset': formset,
			'is_edit': True
		})

	def post(self, request, pk):
		record = PPEIssueRecord.objects.get(pk=pk)

		form = PPEIssueRecordForm(request.POST, instance=record)
		formset = PPEItemFormSet(request.POST, instance=record)

		if form.is_valid() and formset.is_valid():
			form.save()
			formset.save()

			messages.success(request, 'PPE record updated successfully.')
			return redirect('ppe_records:ppe-detail', pk=record.pk)

		return render(request, self.template_name, {
			'form': form,
			'formset': formset,
			'is_edit': True
		})


class PPEIssueDeleteView(DeleteView):
	model = PPEIssueRecord
	template_name = 'ppe_records/ppe_confirm_delete.html'
	success_url = reverse_lazy('ppe_records:ppe-list')
