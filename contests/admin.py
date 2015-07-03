from django.contrib import admin
from .models import Contest, Prize, Entry, Code

from parler.admin import TranslatableAdmin


class PrizeInline(admin.TabularInline):
    '''
        Tabular Inline View for PrizeInline
    '''
    model = Prize
    extra = 1


class CodesInline(admin.TabularInline):
    '''
        Tabular Inline View for CodesInline
    '''
    model = Code
    extra = 1


class ContestAdmin(admin.ModelAdmin):
    '''
        Admin View for Contest
    '''
    list_display = ('title', 'open_date', 'close_date', 'instant_win',)
    list_filter = ('instant_win',)
    inlines = [
        PrizeInline,
        CodesInline,
    ]
    readonly_fields = ('created', 'modified',)
    search_fields = ['title']

admin.site.register(Contest, ContestAdmin)


class EntryAdmin(admin.ModelAdmin):
    '''
        Admin View for Entry
    '''
    list_display = ('email', 'first_name', 'last_name', 'contest','winner', 'prize')
    list_filter = ('contest',)
    raw_id_fields = ('contest',)
    readonly_fields = ('created', 'modified',)
    search_fields = ['email', 'contest', 'first_name', 'last_name']
    save_as = True


admin.site.register(Entry, EntryAdmin)