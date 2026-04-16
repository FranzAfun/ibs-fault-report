from django.contrib import messages
from django.db.models import Count, Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import AssetItemFormSet, AssetRecordForm
from .models import AssetItem, AssetRecord


def _with_mode(url: str, mode: str) -> str:
	if mode:
		return f'{url}?mode={mode}'
	return url


class AssetRecordListView(ListView):
	model = AssetRecord
	context_object_name = 'asset_records'
	template_name = 'assets/asset_list.html'
	paginate_by = 25

	def get_queryset(self):
		return AssetRecord.objects.prefetch_related('items').annotate(
			signed_items=Count('items', filter=Q(items__employee_signature=True)),
		).order_by('-created_at', '-id')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['mode'] = self.request.GET.get('mode', '')
		return context


class AssetRecordDetailView(DetailView):
	queryset = AssetRecord.objects.prefetch_related('items')
	context_object_name = 'asset_record'
	template_name = 'assets/asset_detail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['mode'] = self.request.GET.get('mode', '')
		context['has_signed_items'] = self.object.items.filter(employee_signature=True).exists()
		return context


class AssetRecordCreateView(CreateView):
	model = AssetRecord
	form_class = AssetRecordForm
	template_name = 'assets/asset_form.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if self.request.POST:
			context['formset'] = AssetItemFormSet(self.request.POST)
		else:
			context['formset'] = AssetItemFormSet()
		context['mode'] = self.request.GET.get('mode', '')
		context['has_signed_items'] = False
		return context

	def form_valid(self, form):
		context = self.get_context_data()
		formset = context['formset']

		if formset.is_valid():
			self.object = form.save()
			formset.instance = self.object
			formset.save()
			messages.success(self.request, 'Asset record created successfully.')
			return HttpResponseRedirect(self.get_success_url())

		return self.render_to_response(self.get_context_data(form=form))

	def get_success_url(self):
		mode = self.request.GET.get('mode', '')
		detail_url = reverse_lazy('assets:asset-detail', kwargs={'pk': self.object.pk})
		return _with_mode(str(detail_url), mode)


class AssetRecordUpdateView(UpdateView):
	model = AssetRecord
	form_class = AssetRecordForm
	template_name = 'assets/asset_form.html'

	def _locked(self, record: AssetRecord) -> bool:
		return record.items.filter(employee_signature=True).exists()

	def _locked_redirect(self, record: AssetRecord):
		mode = self.request.GET.get('mode', '')
		messages.warning(self.request, 'This asset record cannot be edited because at least one item is signed.')
		detail_url = reverse('assets:asset-detail', kwargs={'pk': record.pk})
		return redirect(_with_mode(detail_url, mode))

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		if self._locked(self.object):
			return self._locked_redirect(self.object)
		return super().get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		if self._locked(self.object):
			return self._locked_redirect(self.object)
		return super().post(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if self.request.POST:
			context['formset'] = AssetItemFormSet(self.request.POST, instance=self.object)
		else:
			context['formset'] = AssetItemFormSet(instance=self.object)
		context['mode'] = self.request.GET.get('mode', '')
		context['has_signed_items'] = self._locked(self.object)
		return context

	def form_valid(self, form):
		context = self.get_context_data()
		formset = context['formset']

		if formset.is_valid():
			self.object = form.save()
			formset.instance = self.object
			formset.save()
			messages.success(self.request, 'Asset record updated successfully.')
			return HttpResponseRedirect(self.get_success_url())

		return self.render_to_response(self.get_context_data(form=form))

	def get_success_url(self):
		mode = self.request.GET.get('mode', '')
		detail_url = reverse_lazy('assets:asset-detail', kwargs={'pk': self.object.pk})
		return _with_mode(str(detail_url), mode)


class AssetRecordDeleteView(DeleteView):
	model = AssetRecord
	success_url = reverse_lazy('assets:asset-list')
	http_method_names = ['post']

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		mode = request.GET.get('mode', '')

		if self.object.items.filter(employee_signature=True).exists():
			messages.warning(request, 'This asset record cannot be deleted because at least one item is signed.')
			detail_url = reverse('assets:asset-detail', kwargs={'pk': self.object.pk})
			return redirect(_with_mode(detail_url, mode))

		reference_number = self.object.reference_number
		self.object.delete()
		messages.success(request, f'Asset record {reference_number} was deleted successfully.')
		return HttpResponseRedirect(_with_mode(str(self.get_success_url()), mode))


class AssetItemSignView(View):
	http_method_names = ['post']

	def post(self, request, item_id):
		item = get_object_or_404(AssetItem, id=item_id)
		mode = request.GET.get('mode', '')

		if mode == 'staff' and not item.employee_signature:
			item.employee_signature = True
			item.save(update_fields=['employee_signature'])
			messages.success(request, 'Asset item signed successfully.')
		elif mode != 'staff':
			messages.warning(request, 'Only staff mode can sign asset items.')

		detail_url = reverse('assets:asset-detail', kwargs={'pk': item.asset_record_id})
		return redirect(_with_mode(detail_url, mode))
