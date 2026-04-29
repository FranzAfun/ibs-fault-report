from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import CheckbookEntryForm
from .models import CheckbookEntry


class CheckbookListView(ListView):
	model = CheckbookEntry
	template_name = 'checkbook/checkbook_list.html'
	context_object_name = 'entries'


class CheckbookDetailView(DetailView):
	model = CheckbookEntry
	template_name = 'checkbook/checkbook_detail.html'
	context_object_name = 'entry'


class CheckbookCreateView(CreateView):
	model = CheckbookEntry
	form_class = CheckbookEntryForm
	template_name = 'checkbook/checkbook_form.html'
	success_url = reverse_lazy('checkbook:list')

	def form_valid(self, form):
		response = super().form_valid(form)
		messages.success(self.request, 'Checkbook entry created successfully.')
		return response


class CheckbookUpdateView(UpdateView):
	model = CheckbookEntry
	form_class = CheckbookEntryForm
	template_name = 'checkbook/checkbook_form.html'
	success_url = reverse_lazy('checkbook:list')

	def form_valid(self, form):
		response = super().form_valid(form)
		messages.success(self.request, 'Checkbook entry updated successfully.')
		return response


class CheckbookDeleteView(DeleteView):
	model = CheckbookEntry
	success_url = reverse_lazy('checkbook:list')
	http_method_names = ['post']

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		reference_number = self.object.reference_number
		self.object.delete()
		messages.success(request, f'Checkbook entry {reference_number} was deleted successfully.')
		return HttpResponseRedirect(self.success_url)
