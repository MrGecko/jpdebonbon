# -*- coding: utf-8 -*-
from django.db import models
import datetime
# Create your models here.
class Page(models.Model):
    titre = models.CharField(max_length=128)
    proprietaire = models.CharField(max_length=30)
    joueur = models.CharField(max_length=30)
    premier_recit = models.ForeignKey('Recit', related_name="premier_recit", null=True, blank=True)
    
    def __unicode__(self):
        return self.titre

    def recits(self):
        return [self.premier_recit] + self.premier_recit.suivants()
    
    
class Recit(models.Model):
    page = models.ForeignKey(Page)
    description = models.TextField()
    publication_date = models.DateTimeField("Date de publication")
    
    def __unicode__(self):
        return self.description  
      
    def piste_choisie(self):
        return Piste.objects.filter(recit_source=self, choix=True)
  
    def pistes(self):
        return Piste.objects.filter(recit_source=self)   
    
    def nombre_pistes(self):
        return len(self.pistes())
    """
    def reset_choix(self):
        for p in self.pistes():
            p.choix = False
        self.save()
    """   
    def suivant(self):
        piste = self.piste_choisie()
        if len(piste) > 0: 
            return piste[0].recit_destination
        else:
            return None
            
            
    def suivants(self):
        recit = self.suivant()
        liste_recits_suivants = []
        while recit is not None:
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
    """
    def choisir(self):
        self.recit_source.reset_choix()
        self.choix = True
        return self.save()
    """ 
    def __unicode__(self):
        return self.texte
    
