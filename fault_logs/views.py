from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import FaultReportForm
from .models import FaultReport


class FaultReportListView(ListView):
    model = FaultReport
    context_object_name = 'fault_reports'
    template_name = 'fault_logs/report_list.html'
    paginate_by = 25


class FaultReportDetailView(DetailView):
    model = FaultReport
    context_object_name = 'fault_report'
    template_name = 'fault_logs/report_detail.html'


class FaultReportCreateView(CreateView):
    model = FaultReport
    form_class = FaultReportForm
    template_name = 'fault_logs/report_form.html'

    def get_success_url(self):
        return reverse_lazy('fault_logs:faultreport-detail', kwargs={'pk': self.object.pk})


class FaultReportUpdateView(UpdateView):
    model = FaultReport
    form_class = FaultReportForm
    template_name = 'fault_logs/report_form.html'

    def get_success_url(self):
        return reverse_lazy('fault_logs:faultreport-detail', kwargs={'pk': self.object.pk})


class FaultReportDeleteView(DeleteView):
    model = FaultReport
    success_url = reverse_lazy('fault_logs:faultreport-list')
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        reference_number = self.object.reference_number
        self.object.delete()
        messages.success(request, f'Fault report {reference_number} was deleted successfully.')
        return HttpResponseRedirect(self.get_success_url())
