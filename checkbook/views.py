from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import CheckbookEntryForm
from .models import CheckbookEntry


class CheckbookListView(ListView):
	model = CheckbookEntry
	template_name = 'checkbook/checkbook_list.html'
	context_object_name = 'entries'
	paginate_by = 25


class CheckbookDetailView(DetailView):
	model = CheckbookEntry
	template_name = 'checkbook/checkbook_detail.html'
	context_object_name = 'entry'


class CheckbookCreateView(CreateView):
	model = CheckbookEntry
	form_class = CheckbookEntryForm
	template_name = 'checkbook/checkbook_form.html'
	success_url = reverse_lazy('checkbook:list')


class CheckbookUpdateView(UpdateView):
	model = CheckbookEntry
	form_class = CheckbookEntryForm
	template_name = 'checkbook/checkbook_form.html'
	success_url = reverse_lazy('checkbook:list')


class CheckbookDeleteView(DeleteView):
	model = CheckbookEntry
	success_url = reverse_lazy('checkbook:list')
