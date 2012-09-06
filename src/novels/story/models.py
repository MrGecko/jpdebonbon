# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
#import datetime



class Page(models.Model):
    titre = models.CharField(max_length=128)
    titre_url = models.SlugField()
    proprietaire = models.ForeignKey(User, related_name="proprietaire")
    joueur = models.ForeignKey(User, related_name="joueur")
    premier_recit = models.ForeignKey('Recit', related_name="premier_recit", null=True, blank=True)
    
    class Meta:
        unique_together = ("titre_url", "proprietaire", "joueur")
    
    def __unicode__(self):
        return "%s (%s/%s)" % (self.titre, self.proprietaire.username, self.joueur.username)

    def recits(self):
        if not self.premier_recit.disponible or self.premier_recit is None:
            return []
        else:
            return [self.premier_recit] + self.premier_recit.suivants()
        
    def dupliquer(self, joueur):
        #opened = []
        #closed = []
        p = Page(titre=self.titre, titre_url=self.titre_url,
                proprietaire=self.proprietaire, joueur=joueur)
        p.save() #on save une première fois pour avoir un page_id
        #dupliquer les récits
        #closed_list = []
        p.premier_recit = self.premier_recit.dupliquer(p)
        p.save()
        return p
    
    
class Recit(models.Model):
    page = models.ForeignKey(Page)
    description = models.TextField()
    publication_date = models.DateTimeField("Date de publication")
    karma = models.IntegerField("Karma", default=0)
    disponible = models.BooleanField("Est disponible", False)
    
    def dupliquer(self, page):
        recit = Recit(page=page, description=self.description,
                      publication_date=self.publication_date,
                      karma=self.karma, disponible=self.disponible)
        recit.save()
        #closed_list.append(recit)
        #print closed_list
        #dupliquer les pistes
        pistes = self.pistes()
        for piste in pistes:
            piste.dupliquer(recit)

        return recit
    
    def __unicode__(self):
        if len(self.description) > 140:
            desc = self.description[:139]
        else:
            desc = self.description
        return "%s - %s" % (self.page, desc) 
      
    def piste_choisie(self):
        return Piste.objects.filter(recit_source=self, choix=True)
  
    def pistes(self):
        return Piste.objects.filter(recit_source=self)   
    
    def nombre_pistes(self):
        return len(self.pistes())
    
    def ouvert(self):
        return len(self.piste_choisie()) == 0

    def suivant(self):
        piste = self.piste_choisie()
        if len(piste) > 0: 
            return piste[0].recit_destination
        else:
            return None
            
            
    def suivants(self):
        recit = self.suivant()
        liste_recits_suivants = []
        while recit is not None and recit.disponible:
            liste_recits_suivants.append(recit)
            recit = recit.suivant() 
            #print liste_recits_suivants               
        return liste_recits_suivants


class Piste(models.Model):
    #le recit qui precede la piste
    recit_source = models.ForeignKey(Recit, related_name="sources")
    #le recit auquel mene la piste
    recit_destination = models.ForeignKey(Recit, related_name="destinations", null=True, blank=True)
    #le texte de la piste
    texte = models.TextField(max_length=512)
    #la piste a-t-elle ete choisie
    choix = models.BooleanField(default=False)
    #demander au joueur de rentrer une reponse
    demander = models.BooleanField(default=False)
    #reponse possible du joueur
    reponse = models.TextField(max_length=512, blank=True)
    
    karma = models.IntegerField("Karma", default=0)
    min_karma = models.IntegerField("Karma minimum", default= -1000)
    max_karma = models.IntegerField("Karma maximum", default=1000)

    def __unicode__(self):
        return "%i - %s" % (self.id, self.texte)
    
    
    def dupliquer(self, recit):
        #tjrs dupliquer ? il faut ouvrir les pistes quand deja dans closed liste 
        #if self.recit_destination in closed_list:
        #    recit_dest = self.recit_destination.dupliquer(recit.page, closed_list)
        #else:
        #if self.recit_destination is None:
        #    recit_dest = None
        #else:
        #    recit_dest = self.recit_destination.dupliquer(recit.page, closed_list)
        
        piste = Piste(recit_source=recit,
                      recit_destination=self.recit_destination,
                      texte=self.texte,
                      choix=False,
                      demander=self.demander,
                      reponse="",
                      karma=self.karma,
                      min_karma=self.min_karma,
                      max_karma=self.max_karma)
        piste.save()
        return piste
    
    
