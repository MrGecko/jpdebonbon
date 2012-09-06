# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as login_user
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist


from novels.story.models import Page, Recit, Piste



@ensure_csrf_cookie
def login(request):


    
    next_url = "/home/"
    if request.method == "POST":
        if "username" in request.POST and "password" in request.POST:
            user = authenticate(username=request.POST["username"], password=request.POST["password"])
            if user is not None:
                if user.is_active:
                    login_user(request, user)
                    next_url = request.POST["next"]
                    if "?" in next_url:
                        next_url = next_url[:next_url.index("?")]
                else: 
                    next_url = "/home/?etat=inactif"
            else:
                next_url = "/home/?etat=incorrect"
    
    return HttpResponseRedirect(next_url)    


@ensure_csrf_cookie
def home(request):
    if request.user.is_authenticated():
        mes_pages = Page.objects.filter(joueur=request.user)
        message = None
    else:
        mes_pages = []
        message = ""#"Connectez-vous pour pouvoir participer à une histoire"
        if "etat" in request.GET:
            if request.GET["etat"] == "incorrect":
                message = "Votre nom et/ou votre mot de passe sont incorrects." 
            elif request.GET["etat"] == "inactif":
                message = "Votre compte utilisateur est inactif"

    user = request.user
    pages_anonymes = [page for page in Page.objects.filter(joueur__username="anonyme") 
                        if (page.premier_recit.disponible and page.premier_recit is not None and 
                            page.titre_url not in [ma_page.titre_url for ma_page in mes_pages])]
    
    context = {"user" : user, "message" : message,
               "current_url" :  request.get_full_path(),
               "pages_anonymes" : pages_anonymes,
               "mes_pages" : mes_pages}
    
    return render_to_response("story/home.html", context_instance=RequestContext(request, context))
    
    
    
    
    
@ensure_csrf_cookie
def recit(request, titre_url, piste_id):

    save = request.user.is_authenticated()
        #HttpResponseRedirect("/home/?etat=incorrect")
    #else:
    #choix du theme pour le recit renvoyé
    theme = None
    if request.method == "POST":
        if "theme" in request.POST:
            if request.POST["theme"] == "theme_2":
                theme = "theme_1"
            else:
                theme = "theme_2"
                
            
    piste = Piste.objects.get(id=piste_id)  
    print piste
    try:
        page_courante = Page.objects.get(titre_url=titre_url, joueur__username=request.user.username)  
    except Exception:
        page_courante = Page.objects.get(titre_url=titre_url, joueur__username="anonyme")
    #if piste.recit_source.page.joueur is not request.user:
    #    HttpResponseRedirect("/home/?etat=incorrect") 
    print page_courante    
    if piste.recit_source.page is not page_courante:
        #dupliquer le récit pour ce joueur
        if piste.recit_destination is not None:
            if save:
                recit_destination = piste.recit_destination.dupliquer(page_courante)
            else:
                recit_destination = piste.recit_destination
            print "creation : ", recit_destination
        else:
            recit_destination = None
    #choisir la piste cliquée
    #for p in piste.recit_source.pistes():
    #    p.choix = False
    print "dest : ", recit_destination
    
    if piste.demander and request.method == "POST":
        if "reponse" in request.POST:
            piste.reponse = request.POST["reponse"]

    piste.recit_destination = recit_destination
    if save:
        piste.choix = True
        piste.save()

    if  piste.recit_destination is not None:
        #modification du karma
        piste.recit_destination.karma = piste.recit_source.karma + piste.karma
        if save:
            piste.recit_destination.save()    
        
        context = {'recit': piste.recit_destination, 'piste_theme' : theme, }
        template = 'story/pages/recit.html'    
    else:
        context = {'piste_theme' : theme, }
        template = 'story/pages/attente.html'
    
    return render_to_response(template, context_instance=RequestContext(request, context))


#@login_required
@ensure_csrf_cookie
def page(request, titre_url):
    if  request.user.is_authenticated():
        message = None
        username = request.user.username
        
        #récupération de la page du joueur
        try:    
            p = Page.objects.get(titre_url=titre_url, joueur__username=username)  
        except ObjectDoesNotExist:
            #====== cette page n'existe pas pour ce joueur: essayer de la créer
            p_base = Page.objects.get(titre_url=titre_url, joueur__username="anonyme")  
            p = p_base.dupliquer(request.user)
            
            #TODO: copier le premier récit et les suivants... (close/open list ?)
            #p = p_base
        
    else:
        #pas authentifié, récupération de la page anonyme
        message = ""#"Connectez-vous pour pouvoir participer à une histoire"
        p = Page.objects.get(titre_url=titre_url, joueur__username="anonyme")
    
    recits = p.recits()

    if (len(recits) > 0) and (not recits[-1].ouvert()):
        recits.append(False) #en attente de la suite de l'histoire 
        
    context = {'page' : p, 'recits': recits,
               'user' : request.user, "message" : message,
               "current_url" :  request.get_full_path() }
    
    return render_to_response('story/pages/page.html',
                              context_instance=RequestContext(request, context))


@ensure_csrf_cookie
def premiere_description(request, titre_url):
    try:
        page = Page.objects.get(titre_url=titre_url, joueur__username=request.user.username)
    except ObjectDoesNotExist:
        #cette page n'existe pas pour ce joueur
        page = Page.objects.get(titre_url=titre_url, joueur__username="anonyme")
    description = page.premier_recit.description
    if len(description) > 512:
        description = description[:511]
        try:
            description = description[:description.rindex(" ") - 1] + "..."
        except:
            pass
    return HttpResponse(description)

@ensure_csrf_cookie
def reset(request, titre_url):
    if  request.user.is_authenticated():
        username = request.user.username
    else:
        username = "anonyme" 
        
    try:    
        p = Page.objects.get(titre_url=titre_url, joueur__username=username)  
    except ObjectDoesNotExist:
        p = Page.objects.get(titre_url=titre_url, joueur__username="anonyme")  
        
    derniers_recits = Recit.objects.filter(page=p)
    for recit in derniers_recits:
        
        if recit.reference is not None:
            for piste in Piste.objects.filter(recit_destination=recit):
                piste.recit_destination = recit.reference
                piste.choix = False
                piste.save()
            recit.delete()
        else:
            recit.karma = 0
            for piste in recit.pistes():
                piste.choix = False
                piste.save()
                recit.save()

    return page(request, titre_url)


#================================================================
# 
#================================================================


