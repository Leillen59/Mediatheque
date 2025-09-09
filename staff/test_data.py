from staff.models import Livre, DVD, CD, JeuDePlateau, Emprunteur

def run():

    # Emprunteurs
    alice = Emprunteur.objects.create(nom="Alice")
    bob = Emprunteur.objects.create(nom="Bob")
    charlie = Emprunteur.objects.create(nom="Charlie")
    david = Emprunteur.objects.create(nom="David")
    emma = Emprunteur.objects.create(nom="Emma")

    # Livres
    Livre.objects.create(titre="1984", auteur="George Orwell", emprunteur=alice)
    Livre.objects.create(titre="Le Seigneur des Anneaux", auteur="J.R.R. Tolkien")
    Livre.objects.create(titre="Harry Potter", auteur="J.K. Rowling", emprunteur=bob)
    Livre.objects.create(titre="Les Misérables", auteur="Victor Hugo")
    Livre.objects.create(titre="Le Petit Prince", auteur="Antoine de Saint-Exupéry")

    # DVD
    DVD.objects.create(titre="Inception", realisateur="Christopher Nolan")
    DVD.objects.create(titre="Le Parrain", realisateur="Francis Ford Coppola", emprunteur=charlie)
    DVD.objects.create(titre="Matrix", realisateur="Wachowski")
    DVD.objects.create(titre="Gladiator", realisateur="Ridley Scott")
    DVD.objects.create(titre="Titanic", realisateur="James Cameron", emprunteur=alice)

    # CD
    CD.objects.create(titre="Thriller", artiste="Michael Jackson")
    CD.objects.create(titre="Back in Black", artiste="AC/DC")
    CD.objects.create(titre="Abbey Road", artiste="The Beatles", emprunteur=emma)
    CD.objects.create(titre="Nevermind", artiste="Nirvana")
    CD.objects.create(titre="Random Access Memories", artiste="Daft Punk")

    # Jeux de plateau
    JeuDePlateau.objects.create(titre="Monopoly", createur="Hasbro")
    JeuDePlateau.objects.create(titre="Cluedo", createur="Anthony Pratt")
    JeuDePlateau.objects.create(titre="Risk", createur="Albert Lamorisse")
    JeuDePlateau.objects.create(titre="Catan", createur="Klaus Teuber")
    JeuDePlateau.objects.create(titre="7 Wonders", createur="Antoine Bauza")

    print("Données de test créées avec succès.")
