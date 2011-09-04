# -*- coding: utf-8 -*-
from story.models import Page, Recit, Piste
from django.contrib import admin


class PisteInline(admin.StackedInline):
    model = Piste
    fk_name = 'recit_source'
    extra = 0
    fieldsets = [
        (None, {'fields': ['recit_destination', 'choix', 'texte', "karma", "min_karma", "max_karma"] }),
        ('Réponse', {'fields': ['demander', 'reponse'], 'classes': ['collapse']}),
    ]

class RecitAdmin(admin.ModelAdmin):
    inlines = [PisteInline]
    list_display = ('id', 'page', 'originel', 'publication_date', 'description')
 
class PageAdmin(admin.ModelAdmin):
    list_display = ('titre', 'titre_url', 'proprietaire', 'joueur', 'premier_recit')
    prepopulated_fields = {"titre_url": ("titre",)}
     
class PisteAdmin(admin.ModelAdmin):
    list_display = ('id', 'texte', 'recit_source', 'recit_destination', 'choix', 'demander')
     
admin.site.register(Recit, RecitAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Piste, PisteAdmin)

