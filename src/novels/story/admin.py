# -*- coding: utf-8 -*-
from story.models import Page, Recit, Piste
from django.contrib import admin


def copier_recit(recit):
    if recit is  None:
        copie = None
    else:
        copie = Recit(page=recit.page, description=recit.description,
                      publication_date=recit.publication_date,
                      karma=recit.karma)
        copie.save()
        
        pistes = Piste.objects.filter(recit_source=recit)
        copier_pistes(copie, pistes)
    return copie
    
def copier_pistes(recit_source, pistes):
    copies = []
    for p in pistes:
        dest = None #pb ici: comment éviter les destination circulaires ?
        copie = Piste(recit_source=recit_source,
                      recit_destination=dest,
                      texte=p.texte,
                      karma=p.karma,
                      min_karma=p.min_karma,
                      max_karma=p.max_karma,
                      choix=False,
                      demander=p.demander,
                      reponse="")
        copie.save()
        copies.append(copie)

    return copies
        


def copier_page(modeladmin, request, queryset):
    for page in queryset: 
        
        copie = Page(titre=page.titre, titre_url="%s_" % page.titre_url,
                     proprietaire=page.proprietaire, joueur=page.joueur,
                     premier_recit=None)
        copie.save()
        
        page.premier_recit.page = copie
        copie.premier_recit = copier_recit(page.premier_recit)
        #copie.premier_recit.page = copie
        copie.save()
        #premier_recit.save()
        
copier_page.short_description = "Créer une copie des pages sélectionnées"



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
    list_display = ('id', 'page', 'description', 'publication_date', "disponible")
 
class PageAdmin(admin.ModelAdmin):
    list_display = ('id', 'titre', 'titre_url', 'proprietaire', 'joueur', 'premier_recit')
    prepopulated_fields = {"titre_url": ("titre",)}
    actions = [copier_page]
     
class PisteAdmin(admin.ModelAdmin):
    list_display = ('id', 'texte', 'recit_source', 'recit_destination', 'choix', 'demander')
     
admin.site.register(Recit, RecitAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Piste, PisteAdmin)

