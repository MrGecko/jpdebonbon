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
    try:
        print "piste saving"
        piste.save()
    except Exception as e:
        print "exception:", e
    
    piste_class = "piste_orange" if couleur_precedente == "vert" else "piste_vert"
    
    print "piste selectionnee : ", piste, piste.choix
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

