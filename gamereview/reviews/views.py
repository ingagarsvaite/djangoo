from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth import login, authenticate
from .forms import GameReviewForm, RegistrationForm
from .models import GameReview, Publisher, Game
from django.views import generic
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.views.generic.edit import FormMixin
from django.db.models import Max

from django.db.models import F


def index(request):
    best_review = GameReview.objects.annotate(
        max_rating=Max('rating')
    ).filter(rating=F('max_rating')).order_by('-date_created').first()

    context = {
        'best_review': best_review,
    }
    return render(request, 'index.html', context)



@csrf_protect
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            if password == password2:
                if User.objects.filter(username=username).exists():
                    messages.error(
                        request, f'Vartotojo vardas {username} užimtas!')
                    return redirect('register')
                else:

                    user = User.objects.create_user(username, email, password)
                    user.save()

                    user = authenticate(username=username, password=password)
                    login(request, user)

                    return redirect('index')
            else:
                messages.error(request, 'Slaptažodžiai nesutampa!')
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})

class PublisherView(generic.ListView):
    model = Publisher
    template_name = 'publishers.html'
    paginate_by = 3


class PublisherDetailView(generic.DetailView):
    model = Publisher
    template_name = 'publisher.html'
    context_object_name = 'publisher'



class GameListView(generic.ListView):
    model = Game
    template_name = 'games.html'
    paginate_by = 3


class GameDetailView(FormMixin, generic.DetailView):
    model = Game
    template_name = 'game.html'
    form_class = GameReviewForm

    # nurodome, kur atsidursime komentaro sėkmės atveju.
    def get_success_url(self):
        return reverse('game', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.game = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super(GameDetailView, self).form_valid(form)

