import json
import datetime
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from sautadet import models
from sautadet import forms
from sautadet import spouts

def home(request):
    try:
        entry = models.Entry.objects.all()[0]
    except IndexError:
        entry = None
    if entry.read:
        entry = None
    return render(request, 'sautadet/home.html', {'entry': entry})

class Feeds(ListView):
    model = models.Feed
feeds = Feeds.as_view()

class FeedAdd(SessionWizardView):
    template_name = 'sautadet/feed_add.html'

    def get_form(self, step=None, data=None, files=None):
        " Not very elegant, more of a hack... "
        if step is None:
            step = self.steps.current
        if step == '1':
            spout_name = self.get_cleaned_data_for_step('0')['spout_name']
            self.form_list['1'] = getattr(spouts, spout_name).Spout.form
        return super().get_form(step, data, files)

    def done(self, form_list, **kwargs):
        feed = models.Feed(
            title = form_list[2].cleaned_data['title'],
            base_score = form_list[2].cleaned_data['base_score'],
            mult_score = form_list[2].cleaned_data['mult_score'],
            spout = form_list[0].cleaned_data['spout_name'],
            spout_options = json.dumps(form_list[1].cleaned_data),
            last_update = datetime.datetime.now() - datetime.timedelta(days=300),
        )
        feed.save()

        tags_name = [i.strip() for i in form_list[2].cleaned_data['tags'].split(',')]
        for tag_name in tags_name:
            try:
                tag = models.Tag.objects.get(name=tag_name)
            except models.Tag.DoesNotExist:
                tag = models.Tag(name=tag_name)
                tag.save()
            feed.tags.add(tag)

        return HttpResponseRedirect(reverse('sautadet-feeds'))

feed_add = FeedAdd.as_view(
    [forms.SpoutSelectForm, forms.EmptyForm, forms.FeedAddForm]
)

class FeedEdit(UpdateView):
    model = models.Feed
    fields = ['title', 'tags', 'base_score', 'mult_score', 'spout', 'spout_options']

feed_edit = FeedEdit.as_view()

class FeedDelete(DeleteView):
    model = models.Feed
    success_url = reverse_lazy('sautadet-feeds')

feed_delete = FeedDelete.as_view()

class FeedEntries(ListView):
    model = models.Entry
    
    def get_queryset(self):
        feed = get_object_or_404(models.Feed, id=self.kwargs['pk'])
        return feed.entries.all().order_by('-date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feed'] = get_object_or_404(models.Feed, id=self.kwargs['pk'])
        return context

feed_entries = FeedEntries.as_view()

def feed_flush(request, pk):
    feed = get_object_or_404(models.Feed, pk=pk)
    feed.entries.all().delete()
    return HttpResponseRedirect(reverse('sautadet-feeds'))

def feed_read(request, pk):
    feed = get_object_or_404(models.Feed, pk=pk)
    feed.entries.all().update(read=True)
    return HttpResponseRedirect(reverse('sautadet-feeds'))

def read(request, pk):
    entry = get_object_or_404(models.Entry, pk=pk)
    entry.read = True
    entry.save()
    return HttpResponseRedirect(reverse('sautadet-home'))
