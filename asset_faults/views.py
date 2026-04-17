from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import AssetFaultAssignForm, AssetFaultReportForm, AssetFaultResolveForm
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

	def dispatch(self, request, *args, **kwargs):
		mode = self.get_mode()
		if mode == 'it':
			messages.warning(request, 'IT mode cannot create fault reports.')
			list_url = reverse('asset_faults:list')
			return redirect(_with_mode(list_url, mode))
		return super().dispatch(request, *args, **kwargs)

	def get_success_url(self):
		list_url = reverse_lazy('asset_faults:list')
		return _with_mode(str(list_url), self.get_mode())


class AssetFaultUpdateView(ModeContextMixin, UpdateView):
    model = AssetFaultReport
    form_class = AssetFaultReportForm
    template_name = 'asset_faults/assetfault_form.html'

    def dispatch(self, request, *args, **kwargs):
        mode = request.GET.get('mode', '')
        obj = self.get_object()

        detail_url = reverse('asset_faults:detail', kwargs={'pk': obj.pk})

        if obj.it_signature:
            messages.warning(request, 'This fault report is locked because it has been signed by IT.')
            return redirect(_with_mode(detail_url, mode))

        if mode == 'it':
            messages.warning(request, 'IT mode cannot edit the full form. Use Assign, Sign, and Resolve actions.')
            return redirect(_with_mode(detail_url, mode))

        if mode == 'staff':
            messages.warning(request, 'Staff mode cannot edit reports after creation.')
            return redirect(_with_mode(detail_url, mode))

        return super().dispatch(request, *args, **kwargs)

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

		detail_url = reverse('asset_faults:detail', kwargs={'pk': self.object.pk})

		if mode in {'staff', 'it'}:
			messages.warning(request, 'Delete action is not available for this role mode.')
			return redirect(_with_mode(detail_url, mode))

		if self.object.it_signature:
			messages.warning(request, 'This fault report is locked because it has been signed by IT.')
			return redirect(_with_mode(detail_url, mode))

		reference_number = self.object.reference_number
		self.object.delete()
		messages.success(request, f'Fault report {reference_number} was deleted successfully.')
		return redirect(_with_mode(str(self.success_url), mode))


class AssetFaultAssignView(ModeContextMixin, UpdateView):
	model = AssetFaultReport
	form_class = AssetFaultAssignForm
	template_name = 'asset_faults/assetfault_assign_form.html'

	def dispatch(self, request, *args, **kwargs):
		self.object = self.get_object()
		mode = self.get_mode()
		detail_url = reverse('asset_faults:detail', kwargs={'pk': self.object.pk})

		if mode != 'it':
			messages.warning(request, 'Only IT mode can assign this report.')
			return redirect(_with_mode(detail_url, mode))

		if self.object.it_signature:
			messages.warning(request, 'This report is already signed and locked. Assignment is no longer available.')
			return redirect(_with_mode(detail_url, mode))

		return super().dispatch(request, *args, **kwargs)

	def get_success_url(self):
		detail_url = reverse_lazy('asset_faults:detail', kwargs={'pk': self.object.pk})
		return _with_mode(str(detail_url), self.get_mode())


class AssetFaultResolveView(ModeContextMixin, UpdateView):
	model = AssetFaultReport
	form_class = AssetFaultResolveForm
	template_name = 'asset_faults/assetfault_resolve_form.html'

	def dispatch(self, request, *args, **kwargs):
		self.object = self.get_object()
		mode = self.get_mode()
		detail_url = reverse('asset_faults:detail', kwargs={'pk': self.object.pk})

		if mode != 'it':
			messages.warning(request, 'Only IT mode can update the resolution date.')
			return redirect(_with_mode(detail_url, mode))

		if not self.object.it_signature:
			messages.warning(request, 'Resolution date can only be set after IT signature.')
			return redirect(_with_mode(detail_url, mode))

		return super().dispatch(request, *args, **kwargs)

	def get_success_url(self):
		detail_url = reverse_lazy('asset_faults:detail', kwargs={'pk': self.object.pk})
		return _with_mode(str(detail_url), self.get_mode())


class AssetFaultSignView(View):
    http_method_names = ['post']

    def post(self, request, pk):
        obj = get_object_or_404(AssetFaultReport, pk=pk)
        mode = request.GET.get('mode', '')

        if mode != 'it' or obj.it_signature:
            return redirect(_with_mode(reverse('asset_faults:detail', kwargs={'pk': pk}), mode))

        obj.it_signature = True
        obj.save(update_fields=['it_signature'])
        messages.success(request, 'IT signature recorded successfully.')

        return redirect(_with_mode(reverse('asset_faults:detail', kwargs={'pk': pk}), 'it'))
