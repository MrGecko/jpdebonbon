# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render_to_response
from jpdebonbon.story.models import Page, Recit, Piste


def recit(request, piste_id, couleur_precedente):
    piste = Piste.objects.get(id=piste_id)
    
    for p in piste.recit_source.pistes():
        p.choix = False
        #p.save()
    piste.choix = True
    
    if piste.recit_destination is None:
        piste.save()
    elif piste.recit_destination.ouvert():
        piste.save()
    else:
        print "recit destination est fermé : ", piste.recit_destination
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
            
        
    piste_class = "piste_orange" if couleur_precedente == "vert" else "piste_vert"
    return render_to_response('story/pages/recit.html',
                               {
                                   'recit': piste.recit_destination,
                                   'piste_class' : piste_class,
                               })

def page(request, page_id):
    p = Page.objects.get(id=page_id)
    derniers_recits = Recit.objects.filter(page=p)#.order_by('-pub_date')#[:10]
    return render_to_response('story/pages/page.html',
                               {
                                   'derniers_recits': derniers_recits,
                                   'page' : p,
                               })


def reset(request, page_id):
    p = Page.objects.get(id=page_id)
    derniers_recits = Recit.objects.filter(page=p)
    for recit in derniers_recits:
        for piste in recit.pistes():
            piste.choix = False
            piste.save()
    return page(request, page_id)

