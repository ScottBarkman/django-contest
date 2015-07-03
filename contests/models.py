from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel,TitleSlugDescriptionModel
from django_extensions.db.fields import ShortUUIDField

from parler.models import TranslatableModel, TranslatedFields
from .logic import instant_win, prizes_available
from .choices import CODE_TYPES


class Contest(TimeStampedModel, TitleSlugDescriptionModel):
    # translations = TranslatedFields(
    #     location=models.CharField(_('Contest'), max_length=50, blank=False)
    # )

    open_date = models.DateTimeField(_("Starting Date"), help_text='Date entries open', blank=True, null=True)
    close_date = models.DateTimeField(_("Ending Date"), help_text='Date entries close', blank=True, null=True)
    award_date = models.DateTimeField(
        _("Award Date"), help_text='Date prizes are awarded', blank=True, null=True)
    instant_win = models.BooleanField(_("Instant Win"), default=False)
    instant_win_odds = models.IntegerField(
        _("Instant Win Odds"), help_text='1 in ____. Enter whole number', blank=True, null=True)
    daily = models.BooleanField(_("Daily Prizes"), default=False, help_text="A new winner can be won daily")
    code_type = models.CharField(_("Code Type"), default="none", choices=CODE_TYPES, max_length=30)

    class Meta:
        verbose_name = _("Contest")
        verbose_name_plural = _("Contests")

    def __unicode__(self):
        return '%s' % self.title

    _prizes_available = False

    def prizes_available(self):
        if not self._prizes_available:
            self._prizes_available = prizes_available(self)
        return self._prizes_available


class Code(TimeStampedModel):
    code = models.CharField(
        "Code", max_length=100, help_text='A code that has to be present at time of submission')
    contest = models.ForeignKey(Contest)


    class Meta:
        verbose_name = _("Code")
        verbose_name_plural = _("Codes")

    def __unicode__(self):
        return '%s' % self.code


class Prize(TimeStampedModel):
    name = models.CharField(_("Prize"), max_length=150)
    description = models.TextField(_("Description"), default="")
    image = models.ImageField(_("Image"), upload_to='contest/prizes', blank=True, null=True)
    date_available = models.DateField(
        _("Date Prize is Available"), blank=True, help_text="Date that the prize is to be awarded")
    number_available = models.IntegerField(_("Number Available"), default=1, blank=True)
    contest = models.ForeignKey(Contest)

    class Meta:
        verbose_name = _("Prize")
        verbose_name_plural = _("Prizes")

    def __unicode__(self):
        return '%s' % self.name


class Entry(TimeStampedModel):
    first_name = models.CharField(_("First Name"), max_length=50)
    last_name = models.CharField(_("Last Name"), max_length=50)
    email = models.EmailField(_("Email"), max_length=150, )
    code = models.CharField(_("Code"), max_length=25)
    contest = models.ForeignKey(Contest,)
    winner = models.BooleanField(_("Winner"), default=False)
    prize = models.ForeignKey(Prize, blank=True, null=True, on_delete=models.SET_NULL)

    uuid = ShortUUIDField(_("UUID"))

    class Meta:
        verbose_name = _("Entry")
        verbose_name_plural = _("Entries")

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        new = False
        if not self.id:
            new = True

        super(Entry, self).save(*args, **kwargs)
        if self.contest.instant_win and new:
            instant_win(self)
