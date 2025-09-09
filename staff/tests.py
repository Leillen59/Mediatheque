from django.test import TestCase
from django.utils import timezone
from staff.models import Livre, DVD, CD, JeuDePlateau, Emprunteur
from datetime import timedelta

#Test des fonctionnalités principales de l'application
class BibliothequeTests(TestCase):

    def setUp(self):
        # Création emprunteur
        self.alice = Emprunteur.objects.create(nom="Alice")
        self.bob = Emprunteur.objects.create(nom="Bob")

        # Création de données médias
        self.livre = Livre.objects.create(titre="1984", auteur="George Orwell")
        self.dvd = DVD.objects.create(titre="Inception", realisateur="Christopher Nolan")
        self.cd = CD.objects.create(titre="Thriller", artiste="Michael Jackson")
        self.jeu = JeuDePlateau.objects.create(titre="Monopoly", createur="Hasbro")

    def test_emprunt_media(self):
        """Un média devient indisponible lorsqu'il est emprunté"""
        self.livre.emprunteur = self.alice
        self.livre.save()
        self.assertFalse(self.livre.disponible)
        self.assertIsNotNone(self.livre.dateEmprunt)

    def test_retour_media(self):
        """Le retour d’un média supprime l’emprunteur et la date"""
        self.dvd.emprunteur = self.bob
        self.dvd.save()
        self.dvd.emprunteur = None
        self.dvd.save()
        self.assertTrue(self.dvd.disponible)
        self.assertIsNone(self.dvd.dateEmprunt)

    def test_blocage_apres_3_emprunts(self):
        """Un emprunteur est bloqué après 3 emprunts"""
        for i in range(3):
            Livre.objects.create(titre=f"Livre {i}", auteur="Test", emprunteur=self.alice)
        self.alice.refresh_from_db()
        self.assertTrue(self.alice.bloque)

    def test_blocage_apres_8_jours(self):
        """Un emprunteur est bloqué après un emprunt > 8 jours"""
        livre = Livre.objects.create(titre="Ancien Livre", auteur="Auteur", emprunteur=self.alice)
        livre.dateEmprunt = timezone.now().date() - timedelta(days=9)
        livre.save()
        self.alice.update_bloque()
        self.assertTrue(self.alice.bloque)

    def test_jeux_ne_peuvent_pas_etre_empruntes(self):
        """Un jeu de plateau ne peut pas être emprunté"""
        self.jeu.emprunteur = self.alice
        self.jeu.save()
        self.assertIsNone(self.jeu.emprunteur)
        self.assertTrue(self.jeu.disponible)
