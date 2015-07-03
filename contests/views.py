from django.views.generic import DetailView, CreateView
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponseRedirect

from .models import Contest, Entry
from .forms import EntryForm, BaseEntryForm


class ContestDetailView(DetailView):

    '''
        Contest Detail View

    '''
    model = Contest
    template_name = "contests/detail.html"

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Contest, slug=self.kwargs['slug'])


class EntryCreateView(CreateView):
    model = Entry
    template_name = "contests/entry.html"
    _contest = None

    def get_context_data(self, *args, **kwargs):
        c = super(EntryCreateView, self).get_context_data(*args, **kwargs)
        c['contest'] = get_object_or_404(Contest, slug=self.kwargs['slug'])

        return c

    def get_form(self, *args, **kwargs):
        contest = get_object_or_404(Contest, slug=self.kwargs['slug'])
        self._contest = contest
        if self._contest.code_type == 'none':
            form = BaseEntryForm(self.request.POST or None, contest=contest, request=self.request)
        else:
            form = EntryForm(self.request.POST or None, contest=contest, request=self.request)
        return form

    def form_valid(self, form):
        c = form.save(commit=False)
        c.contest = self._contest
        c.save()

        print self._contest
        if self._contest.instant_win and c.winner:
            return HttpResponseRedirect(reverse_lazy('contest-winner', args=(self._contest.slug, )))

        return HttpResponseRedirect(reverse_lazy('contest-entry-received', args=(self._contest.slug,)))


class WinnerDetailView(DetailView):
    model = Entry
    template_name = "contests/winner.html"

    _contest = None

    def get_object(self, *args, **kwargs):
        self._contest = get_object_or_404(Contest, slug=self.kwargs['slug'])
        entry = get_object_or_404(Entry, contest=self._contest, uuid=self.kwargs['uuid'], winner=True)
        return entry

    def get_context_data(self, *args, **kwargs):
        c = super(WinnerDetailView, self).get_context_data(*args, **kwargs)
        c['contest'] = self._contest
        return c

class EntryReceivedView(DetailView):
    model = Contest
    template_name = 'contests/entry-received.html'
