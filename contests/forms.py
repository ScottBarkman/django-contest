from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Entry, Code
from datetime import datetime


class BaseEntryForm(forms.ModelForm):

    class Meta:
        model = Entry
        fields = ['first_name', 'last_name', 'email', 'code']

    _contest = None
    _request = None
    def __init__(self, *args, **kwargs):
        self._contest = kwargs.pop('contest', None)
        self._request = kwargs.pop('request', None)

        super(BaseEntryForm, self).__init__(*args, **kwargs)


class EntryForm(BaseEntryForm):

    class Meta:
        model = Entry
        fields = ['first_name', 'last_name', 'email', 'code']

    def clean_code(self, *args, **kwargs):
        code = self.cleaned_data['code']
        today = datetime.today()
        if not Code.objects.filter(code__iexact=code).count():
            raise forms.ValidationError(_("Code is invalid"))

        if self._contest.code_type == 'single':
            if Entry.objects.filter(contest=self._contest, code__iexact=code).count():
                raise forms.ValidationError(_("Code has already been used"))
        elif self._contest.code_type == 'person':
            if Entry.objects.filter(contest=self._contest, code__iexact=code, email__iexact=self.cleaned_data['email']).count():
                raise forms.ValidationError(_("You have already used this code"))
        elif self._contest.code_type == 'day':
            if Entry.objects.filter(contest=self._contest, code__iexact=code, email__iexact=self.cleaned_data['email'], created__year=today.year, created__month=today.month, created__day=today.day).count():
                raise forms.ValidationError(_("You have already used this code today"))

        return code
