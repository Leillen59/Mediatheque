from django.db import models
from django.utils import timezone

class Media(models.Model):
    titre = models.CharField(max_length=150)
    dateEmprunt = models.DateField(blank=True, null=True)
    disponible = models.BooleanField(default=True)
    emprunteur = models.ForeignKey(
        'Emprunteur', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='emprunts')
    
    def save(self, *args, **kwargs):
        self.disponible = self.emprunteur is None
        
        if self.emprunteur and not self.dateEmprunt:
            self.dateEmprunt = timezone.now().date()
        elif not self.emprunteur:
            self.dateEmprunt = None
        
        super(Media, self).save(*args, **kwargs)
        
        if self.emprunteur:
            self.emprunteur.update_bloque()
    def __str__(self):
        return self.titre
    
    @property
    def est_emprunte(self):
        return self.__class__.__name__.lower()

class Livre(Media):
    auteur = models.CharField(max_length=150)

class DVD(Media):
    realisateur = models.CharField(max_length=150)

class CD(Media):
    artiste = models.CharField(max_length=150)

class JeuDePlateau(Media):
    createur = models.CharField(max_length=150)
    
    def save(self, *args, **kwargs):
        self.emprunteur = None
        self.dateEmprunt = None
        self.disponible = True
        super().save(*args, **kwargs)

class Emprunteur(models.Model):
    nom = models.CharField(max_length=150)
    bloque = models.BooleanField(default=False)

    def update_bloque(self):
        """Met à jour le statut de blocage :
        - 3 emprunts simultanés
        - ou un emprunt de plus de 8 jours
        """
        nb_emprunts = self.emprunts.count()
        bloque_par_nombre = nb_emprunts >= 3

        bloque_par_duree = False
        for media in self.emprunts.all():
            if media.dateEmprunt and (timezone.now().date() - media.dateEmprunt).days > 8:
                bloque_par_duree = True
                break

        self.bloque = bloque_par_nombre or bloque_par_duree
        self.save(update_fields=["bloque"])

    def __str__(self):
        return self.nom