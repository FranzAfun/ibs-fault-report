from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import AssetFaultReportForm
from .models import AssetFaultReport


class AssetFaultListView(ListView):
	model = AssetFaultReport
	template_name = 'asset_faults/assetfault_list.html'
	context_object_name = 'records'


class AssetFaultDetailView(DetailView):
	model = AssetFaultReport
	template_name = 'asset_faults/assetfault_detail.html'


class AssetFaultCreateView(CreateView):
	model = AssetFaultReport
	form_class = AssetFaultReportForm
	template_name = 'asset_faults/assetfault_form.html'
	success_url = reverse_lazy('asset_faults:list')


class AssetFaultUpdateView(UpdateView):
	model = AssetFaultReport
	form_class = AssetFaultReportForm
	template_name = 'asset_faults/assetfault_form.html'
	success_url = reverse_lazy('asset_faults:list')


class AssetFaultDeleteView(DeleteView):
	model = AssetFaultReport
	success_url = reverse_lazy('asset_faults:list')
