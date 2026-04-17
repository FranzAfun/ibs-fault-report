from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import AssetFaultReportForm
from .models import AssetFaultReport


def _with_mode(url: str, mode: str) -> str:
	if mode:
		return f'{url}?mode={mode}'
	return url


class ModeContextMixin:
	def get_mode(self) -> str:
		return self.request.GET.get('mode', '')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['mode'] = self.get_mode()
		return context


class AssetFaultListView(ModeContextMixin, ListView):
	model = AssetFaultReport
	template_name = 'asset_faults/assetfault_list.html'
	context_object_name = 'records'

	def get_queryset(self):
		queryset = AssetFaultReport.objects.all()
		mode = self.get_mode()
		if mode == 'staff':
			return queryset
		if mode == 'it':
			return queryset
		return queryset


class AssetFaultDetailView(ModeContextMixin, DetailView):
	model = AssetFaultReport
	template_name = 'asset_faults/assetfault_detail.html'


class AssetFaultCreateView(ModeContextMixin, CreateView):
	model = AssetFaultReport
	form_class = AssetFaultReportForm
	template_name = 'asset_faults/assetfault_form.html'

	def get_success_url(self):
		list_url = reverse_lazy('asset_faults:list')
		return _with_mode(str(list_url), self.get_mode())


class AssetFaultUpdateView(ModeContextMixin, UpdateView):
	model = AssetFaultReport
	form_class = AssetFaultReportForm
	template_name = 'asset_faults/assetfault_form.html'

	def _locked_redirect(self, record: AssetFaultReport):
		mode = self.get_mode()
		messages.warning(self.request, 'This fault report is locked because it has been signed by IT.')
		detail_url = reverse('asset_faults:detail', kwargs={'pk': record.pk})
		return redirect(_with_mode(detail_url, mode))

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		if self.object.it_signature:
			return self._locked_redirect(self.object)
		return super().get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		if self.object.it_signature:
			return self._locked_redirect(self.object)
		return super().post(request, *args, **kwargs)

	def get_success_url(self):
		list_url = reverse_lazy('asset_faults:list')
		return _with_mode(str(list_url), self.get_mode())


class AssetFaultDeleteView(ModeContextMixin, DeleteView):
	model = AssetFaultReport
	success_url = reverse_lazy('asset_faults:list')
	http_method_names = ['post']

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		mode = self.get_mode()

		if self.object.it_signature:
			messages.warning(request, 'This fault report is locked because it has been signed by IT.')
			detail_url = reverse('asset_faults:detail', kwargs={'pk': self.object.pk})
			return redirect(_with_mode(detail_url, mode))

		reference_number = self.object.reference_number
		self.object.delete()
		messages.success(request, f'Fault report {reference_number} was deleted successfully.')
		return redirect(_with_mode(str(self.success_url), mode))


class AssetFaultSignView(View):
	http_method_names = ['post']

	def post(self, request, pk):
		record = get_object_or_404(AssetFaultReport, pk=pk)
		mode = request.GET.get('mode', '')

		if mode == 'it' and not record.it_signature:
			record.it_signature = True
			record.save(update_fields=['it_signature'])
			messages.success(request, 'IT signature recorded successfully.')
		elif mode != 'it':
			messages.warning(request, 'Only IT mode can sign fault reports.')

		detail_url = reverse('asset_faults:detail', kwargs={'pk': record.pk})
		return redirect(_with_mode(detail_url, mode))
