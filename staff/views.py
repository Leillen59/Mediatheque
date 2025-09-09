from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from staff.models import Media, Livre, DVD, CD, JeuDePlateau, Emprunteur
from .forms import LivreForm, DVDForm, CDForm, JeuDePlateauForm, EmprunteurForm
from django.db.models import Count

def est_staff(user):
    return user.is_staff

@login_required(login_url='/')
@user_passes_test(est_staff, login_url='/')
def dashboard(request):
    filtre = request.GET.get("type", "all")
    if filtre == "livre":
        medias = Livre.objects.all()
    elif filtre == "dvd":
        medias = DVD.objects.all()
    elif filtre == "cd":
        medias = CD.objects.all()
    elif filtre == "jeu":
        medias = JeuDePlateau.objects.all()
    else:
        medias = Media.objects.all()
        
    return render(request, 'dashboard.html', {
        'medias': medias, 
        'filtre': filtre
    })

def logout_staff(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/')
@user_passes_test(est_staff, login_url='/')
def ajouter_media(request, type_media):
    form = None
    if type_media == 'livre':
        form = LivreForm(request.POST or None)
    elif type_media == 'dvd':
        form = DVDForm(request.POST or None)
    elif type_media == 'cd':
        form = CDForm(request.POST or None)
    elif type_media == 'jeu':
        form = JeuDePlateauForm(request.POST or None)
    
    if request.method == 'POST' and form and form.is_valid():
        form.save()
        return redirect('/staff/')

    return render(request, 'ajouter_media.html', {
        'form': form,
        'type_media': type_media
        })
    
@login_required(login_url='/')
@user_passes_test(est_staff, login_url='/')
def modifier_media(request, pk):
    media = None
    form_class = None
    
    if Livre.objects.filter(pk=pk).exists():
        media = get_object_or_404(Livre, pk=pk)
        form_class = LivreForm
    elif DVD.objects.filter(pk=pk).exists():
        media = get_object_or_404(DVD, pk=pk)
        form_class = DVDForm
    elif CD.objects.filter(pk=pk).exists():
        media = get_object_or_404(CD, pk=pk)
        form_class = CDForm
    elif JeuDePlateau.objects.filter(pk=pk).exists():
        media = get_object_or_404(JeuDePlateau, pk=pk)
        form_class = JeuDePlateauForm
    
    if not media :
        return render(request, "modifier_media.html", {"form": None, "media": None})
    
    form = form_class(request.POST or None, instance=media)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('/staff/')

    return render(request, 'modifier_media.html', {
        'form': form,
        'media': media
    })

@login_required(login_url='/')
@user_passes_test(est_staff, login_url='/')
def supprimer_media(request, pk):
    media = None
    for model in (Livre, DVD, CD, JeuDePlateau):
        try:
            media = model.objects.get(pk=pk)
            break
        except model.DoesNotExist:
            continue

    if not media:
        return render(request, "supprimer_media.html", {"media": None})

    if request.method == "POST":
        media.delete()
        return redirect("/staff/")

    return render(request, "supprimer_media.html", {"media": media})

@login_required(login_url="/")
@user_passes_test(est_staff, login_url="/")
def liste_emprunteurs(request):
    emprunteurs = Emprunteur.objects.annotate(nb_emprunts=Count("emprunts"))
    return render(request, "liste_emprunteurs.html", {"emprunteurs": emprunteurs})


@login_required(login_url="/")
@user_passes_test(est_staff, login_url="/")
def ajouter_emprunteur(request):
    form = EmprunteurForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("liste_emprunteurs")
    return render(request, "ajouter_emprunteur.html", {"form": form})


@login_required(login_url="/")
@user_passes_test(est_staff, login_url="/")
def modifier_emprunteur(request, pk):
    emprunteur = get_object_or_404(Emprunteur, pk=pk)
    form = EmprunteurForm(request.POST or None, instance=emprunteur)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("liste_emprunteurs")
    return render(request, "modifier_emprunteur.html", {"form": form, "emprunteur": emprunteur})


@login_required(login_url="/")
@user_passes_test(est_staff, login_url="/")
def supprimer_emprunteur(request, pk):
    emprunteur = get_object_or_404(Emprunteur, pk=pk)
    if request.method == "POST":
        emprunteur.delete()
        return redirect("liste_emprunteurs")
    return render(request, "staff/supprimer_emprunteur.html", {"emprunteur": emprunteur})

@login_required(login_url="/")
@user_passes_test(est_staff, login_url="/")
def retour_media(request, pk):
    media = None
    for model in (Livre, DVD, CD):
        try:
            media = model.objects.get(pk=pk)
            break
        except model.DoesNotExist:
            continue

    if not media:
        return redirect("/staff/")

    if request.method == "POST":
        ancien_emprunteur = media.emprunteur
        media.emprunteur = None
        media.dateEmprunt = None
        media.disponible = True
        media.save()

        # mettre à jour blocage de l’ancien emprunteur
        if ancien_emprunteur:
            ancien_emprunteur.update_bloque()

        return redirect("/staff/")

    return render(request, "retour_media.html", {"media": media})