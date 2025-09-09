from django import forms
from .models import Livre, DVD, CD, JeuDePlateau,Emprunteur

class BaseMediaForm(forms.ModelForm):
    dateEmprunt = forms.DateField(disabled=True, required=False, label="Date d'emprunt")

class LivreForm(BaseMediaForm):
    class Meta:
        model = Livre
        fields = ["titre", "auteur", "emprunteur", "dateEmprunt"]

class DVDForm(BaseMediaForm):
    class Meta:
        model = DVD
        fields = ["titre", "realisateur", "emprunteur", "dateEmprunt"]

class CDForm(BaseMediaForm):
    class Meta:
        model = CD
        fields = ["titre", "artiste", "emprunteur", "dateEmprunt"]

class JeuDePlateauForm(BaseMediaForm):
    class Meta:
        model = JeuDePlateau
        fields = ["titre", "createur"]
        
class EmprunteurForm(forms.ModelForm): 
    class Meta: 
        model = Emprunteur 
        fields = ["nom", "bloque"]