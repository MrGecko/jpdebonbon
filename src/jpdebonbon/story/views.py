# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from jpdebonbon.story.models import Page, Recit, Piste
from django.views.decorators.csrf import ensure_csrf_cookie




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
                        publication_date=dest.publication_date)
        nouveau.save()
        piste.recit_destination = nouveau
        piste.save()
        #creation des nouvelles pistes
        for p in dest.pistes():
            nouvelle_piste = Piste(recit_source=nouveau,
                                   recit_destination=p.recit_destination,
                                   texte=p.texte,
                                   choix=False,
                                   demander=p.demander,
                                   reponse="")
            nouvelle_piste.save()
    
     
    theme = None
    if request.method == "POST":
        if "theme" in request.POST:
            if request.POST["theme"] == "theme_2":
                theme = "theme_1"
            else:
                theme = "theme_2"

    return render_to_response('story/pages/recit.html',
                               {
                                   'recit': piste.recit_destination,
                                   'piste_theme' : theme,
                               })




@ensure_csrf_cookie
def page(request, page_id):
    p = Page.objects.get(id=page_id)
    derniers_recits = Recit.objects.filter(page=p)#.order_by('-pub_date')#[:10]
    return render_to_response('story/pages/page.html',
                               {
                                   'derniers_recits': derniers_recits,
                                   'page' : p,
                               })

@ensure_csrf_cookie
def reset(request, page_id):
    p = Page.objects.get(id=page_id)
    derniers_recits = Recit.objects.filter(page=p)
    for recit in derniers_recits:
        for piste in recit.pistes():
            piste.choix = False
            piste.save()
    return page(request, page_id)

