from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.cache import never_cache
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import FaultReportForm
from .models import FaultReport, FaultReportAttachment


class AttachmentUploadMixin:
    def _create_attachments(self, report, uploads):
        created = 0
        for upload in uploads:
            FaultReportAttachment.objects.create(
                fault_report=report,
                file=upload,
                original_name=upload.name,
                file_size=upload.size,
            )
            created += 1
        return created


@method_decorator(never_cache, name='dispatch')
class FaultReportListView(ListView):
    model = FaultReport
    context_object_name = 'fault_reports'
    template_name = 'fault_logs/report_list.html'
    paginate_by = 25

    def get_queryset(self):
        return FaultReport.objects.prefetch_related('attachments')


class FaultReportDetailView(DetailView):
    queryset = FaultReport.objects.prefetch_related('attachments')
    context_object_name = 'fault_report'
    template_name = 'fault_logs/report_detail.html'


class FaultReportCreateView(AttachmentUploadMixin, CreateView):
    model = FaultReport
    form_class = FaultReportForm
    template_name = 'fault_logs/report_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        uploads = form.cleaned_data.get('attachments', [])
        created = self._create_attachments(self.object, uploads)
        if created:
            messages.success(self.request, f'{created} attachment(s) uploaded successfully.')
        return response

    def get_success_url(self):
        return reverse_lazy('fault_logs:faultreport-detail', kwargs={'pk': self.object.pk})


class FaultReportUpdateView(AttachmentUploadMixin, UpdateView):
    model = FaultReport
    form_class = FaultReportForm
    template_name = 'fault_logs/report_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        uploads = form.cleaned_data.get('attachments', [])
        created = self._create_attachments(self.object, uploads)
        if created:
            messages.success(self.request, f'{created} attachment(s) uploaded successfully.')
        return response

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


class FaultReportAttachmentDeleteView(View):
    http_method_names = ['post']

    def post(self, request, pk):
        attachment = get_object_or_404(FaultReportAttachment, pk=pk)
        report_pk = attachment.fault_report_id
        filename = attachment.filename

        if attachment.file:
            attachment.file.delete(save=False)
        attachment.delete()

        messages.success(request, f'Attachment {filename} was deleted successfully.')

        next_url = request.POST.get('next', '').strip()
        if next_url and url_has_allowed_host_and_scheme(
            url=next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            return redirect(next_url)

        return redirect('fault_logs:faultreport-detail', pk=report_pk)
