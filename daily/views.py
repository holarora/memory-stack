from django.views.generic import ListView
from django.views.generic.edit import CreateView

from daily.forms import EntryForm
from .models import Entry

# Create your views here.


class EntryCreateView(CreateView):
    template_name = "daily/create_entry.html"
    model = Entry
    form_class = EntryForm
    success_url = "/daily"

    def form_valid(self, form):
        response = super().form_valid(form)
        print(f"Image uploaded: {form.instance.image.path}")
        return response


class EntryListView(ListView):
    template_name = "daily/all_entries.html"
    model = Entry
    context_object_name = "entries"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_entries'] = Entry.objects.prefetch_related("images").order_by("-date")[:10]
        context['older_entries'] = Entry.objects.prefetch_related("images").order_by("-date")[10:]
        return context
