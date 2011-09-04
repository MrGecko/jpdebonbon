# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie
from novels.story.models import Page, Recit, Piste




@ensure_csrf_cookie
def recit(request, piste_id):
    piste = Piste.objects.get(id=piste_id)
    #choisir la piste cliquée
    for p in piste.recit_source.pistes():
        p.choix = False
    piste.choix = True
    
    if piste.demander and request.method == "POST":
        if "reponse" in request.POST:
            piste.reponse = request.POST["reponse"]


    if piste.recit_destination is None:
        piste.save()
    elif piste.recit_destination.ouvert():
        piste.save()
    else:
        #recit destination déjà utilisé: il faut en faire une copie ouverte
        dest = piste.recit_destination
        nouveau = Recit(page=dest.page,
                        description=dest.description,
                        publication_date=dest.publication_date,
                        karma=dest.karma)
        nouveau.save()
        piste.recit_destination = nouveau
        piste.save()
        #creation des nouvelles pistes
        for p in dest.pistes():
            nouvelle_piste = Piste(recit_source=nouveau,
                                   recit_destination=p.recit_destination,
                                   texte=p.texte,
                                   karma=p.karma,
                                   min_karma=p.min_karma,
                                   max_karma=p.max_karma,
                                   choix=False,
                                   demander=p.demander,
                                   reponse="")
            nouvelle_piste.save()
    
    
    #modification du karma
    if piste.recit_destination is not None:
        piste.recit_destination.karma = piste.recit_source.karma + piste.karma
        piste.recit_destination.save()
   
    #choix du theme pour le recit 
    theme = None
    if request.method == "POST":
        if "theme" in request.POST:
            if request.POST["theme"] == "theme_2":
                theme = "theme_1"
            else:
                theme = "theme_2"


    if piste.recit_destination is not None:
        context = {'recit': piste.recit_destination, 'piste_theme' : theme, }
        return render_to_response('story/pages/recit.html',
                                   context_instance=RequestContext(request, context))
    else:
        context = {'piste_theme' : theme, }
        return render_to_response('story/pages/attente.html',
                                  context_instance=RequestContext(request, context))





@ensure_csrf_cookie
def page(request, titre_url):
    p = Page.objects.get(titre_url=titre_url)
    recits = p.recits()
    if not recits[-1].ouvert():
        recits.append(False)
    
    context = {'page' : p, 'recits': recits, }
    return render_to_response('story/pages/page.html',
                              context_instance=RequestContext(request, context))

@ensure_csrf_cookie
def reset(request, titre_url):
    p = Page.objects.get(titre_url=titre_url)
    derniers_recits = Recit.objects.filter(page=p)
    for recit in derniers_recits:
        recit.karma = 0
        for piste in recit.pistes():
            piste.choix = False
            piste.save()
        recit.save()
    return page(request, page_id)

