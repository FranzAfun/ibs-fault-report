from django.contrib import messages
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import DetailView, ListView

from .forms import PPEIssueRecordForm, PPEItemFormSet
from .models import PPEIssueRecord, PPEItem


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

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['mode'] = self.request.GET.get('mode', '')
		context['has_signed_items'] = self.object.items.exclude(employee_signature='').exists()
		return context


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
			record = form.save(commit=False)
			if request.user.is_authenticated:
				record.created_by = request.user
			record.save()

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
		record = get_object_or_404(PPEIssueRecord, pk=pk)

		# block editing once any item is signed
		if record.items.exclude(employee_signature='').exists():
			messages.warning(request, 'This PPE record cannot be edited because at least one item is signed.')
			return redirect('ppe_records:ppe-detail', pk=record.id)

		form = PPEIssueRecordForm(instance=record)
		formset = PPEItemFormSet(instance=record)

		return render(request, self.template_name, {
			'form': form,
			'formset': formset,
			'is_edit': True
		})

	def post(self, request, pk):
		record = get_object_or_404(PPEIssueRecord, pk=pk)

		# block editing once any item is signed
		if record.items.exclude(employee_signature='').exists():
			messages.warning(request, 'This PPE record cannot be edited because at least one item is signed.')
			return redirect('ppe_records:ppe-detail', pk=record.id)

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


class PPEIssueDeleteView(View):
	template_name = 'ppe_records/ppe_confirm_delete.html'
	success_url = reverse_lazy('ppe_records:ppe-list')

	def get(self, request, pk):
		record = PPEIssueRecord.objects.filter(pk=pk).first()
		if not record:
			messages.warning(request, 'PPE record no longer exists.')
			return redirect(self.success_url)

		# block delete once any item is signed
		if record.items.exclude(employee_signature='').exists():
			messages.warning(request, 'This PPE record cannot be deleted because at least one item is signed.')
			return redirect('ppe_records:ppe-detail', pk=record.id)

		return render(request, self.template_name, {'object': record})

	def post(self, request, pk):
		record = PPEIssueRecord.objects.filter(pk=pk).first()

		if record:
			# block delete once any item is signed
			if record.items.exclude(employee_signature='').exists():
				messages.warning(request, 'This PPE record cannot be deleted because at least one item is signed.')
				return redirect('ppe_records:ppe-detail', pk=record.id)

			record_name = record.employee_name
			record.delete()
			messages.success(request, f'PPE record for {record_name} deleted successfully.')
		else:
			messages.warning(request, 'PPE record was already deleted or no longer exists.')

		return redirect(self.success_url)


def sign_ppe_item(request, item_id):
	item = get_object_or_404(PPEItem, id=item_id)
	mode = request.GET.get('mode')

	if request.method == 'POST':
		if mode == 'staff' and not item.employee_signature:
			item.employee_signature = True
			item.save(update_fields=['employee_signature'])

	return redirect(f'/ppe/{item.ppe_record.id}/?mode={mode}')
