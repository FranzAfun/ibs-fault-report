from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import AssetItemFormSet, AssetRecordForm
from .models import AssetRecord


class AssetRecordListView(ListView):
	model = AssetRecord
	context_object_name = 'asset_records'
	template_name = 'assets/asset_list.html'
	paginate_by = 25

	def get_queryset(self):
		return AssetRecord.objects.prefetch_related('items').order_by('-created_at', '-id')


class AssetRecordDetailView(DetailView):
	queryset = AssetRecord.objects.prefetch_related('items')
	context_object_name = 'asset_record'
	template_name = 'assets/asset_detail.html'


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

		return self.form_invalid(form)

	def get_success_url(self):
		return reverse_lazy('assets:asset-detail', kwargs={'pk': self.object.pk})


class AssetRecordUpdateView(UpdateView):
	model = AssetRecord
	form_class = AssetRecordForm
	template_name = 'assets/asset_form.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if self.request.POST:
			context['formset'] = AssetItemFormSet(self.request.POST, instance=self.object)
		else:
			context['formset'] = AssetItemFormSet(instance=self.object)
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

		return self.form_invalid(form)

	def get_success_url(self):
		return reverse_lazy('assets:asset-detail', kwargs={'pk': self.object.pk})


class AssetRecordDeleteView(DeleteView):
	model = AssetRecord
	success_url = reverse_lazy('assets:asset-list')
	http_method_names = ['post']

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		reference_number = self.object.reference_number
		self.object.delete()
		messages.success(request, f'Asset record {reference_number} was deleted successfully.')
		return HttpResponseRedirect(self.get_success_url())
