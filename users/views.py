from django.shortcuts import render
from staff.models import Media, Livre, DVD, CD, JeuDePlateau

from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib import messages

def home(request):
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
        
    return render(request, 'home.html', {
        'medias': medias, 
        'filtre': filtre
    })
    
def login_staff(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('/staff/')
            else:
                messages.error(request, "Identifiants non valides")
        else:
            messages.error(request, "Identifiants invalides.")
            return redirect('/')
    
    return render(request, 'home.html')