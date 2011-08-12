# -*- coding: utf-8 -*-
from story.models import Page, Recit, Piste
from django.contrib import admin


class PisteInline(admin.StackedInline):
    model = Piste
    fk_name = 'recit_source'
    extra = 0
    fieldsets = [
        (None, {'fields': ['recit_destination', 'choix', 'texte'] }),
        ('Réponse', {'fields': ['demander', 'reponse'], 'classes': ['collapse']}),
    ]

class RecitAdmin(admin.ModelAdmin):
    inlines = [PisteInline]
    list_display = ('page', 'publication_date', 'description')
 
class PageAdmin(admin.ModelAdmin):
    list_display = ('titre', 'proprietaire', 'joueur', 'premier_recit')
     
class PisteAdmin(admin.ModelAdmin):
    list_display = ('texte', 'recit_source', 'recit_destination', 'choix', 'demander')
     
admin.site.register(Recit, RecitAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Piste, PisteAdmin)

