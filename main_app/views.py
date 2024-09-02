from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Cat, Toy
from .forms import FeedingForm

# Create your views here.
# def home(request):
#     return render(request, 'home.html')

class Home(LoginView):
    template_name = 'home.html'

def about(request):
    return render(request, 'about.html')

@login_required
def cat_index(request):
    # cats = Cat.objects.all()
    cats = Cat.objects.filter(user=request.user)
    return render(request, 'cats/index.html', {'cats': cats})

@login_required
def cat_detail(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    # toys = Toy.objects.all()
    toys_cat_doesnt_have = Toy.objects.exclude(id__in = cat.toys.all().values_list('id'))
    feeding_form = FeedingForm()
    return render(request, 'cats/detail.html', {
        'cat': cat,
        'feeding_form': feeding_form,
        'toys': toys_cat_doesnt_have
        })

class CatCreate(LoginRequiredMixin, CreateView):
    model = Cat
    fields = ['name', 'breed', 'description', 'age']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    success_url = '/cats/'

class CatUpdate(LoginRequiredMixin, UpdateView):
    model = Cat
    fields = ['breed', 'description', 'age']

class CatDelete(LoginRequiredMixin, DeleteView):
    model = Cat
    success_url = '/cats/'

@login_required
def add_feeding(request, cat_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.cat_id = cat_id
        new_feeding.save()

    return redirect('cat-detail', cat_id=cat_id)

class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = '__all__'

class ToyList(LoginRequiredMixin, ListView):
    model = Toy

class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy

class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ['name', 'color']

class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = '/toys/'

@login_required
def associate_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect('cat-detail', cat_id=cat_id)

@login_required
def remove_toy(request, cat_id, toy_id):
    # Look up the cat
    cat = Cat.objects.get(id=cat_id)
    # Look up the toy
    toy = Toy.objects.get(id=toy_id)
    # Remove the toy from the cat
    cat.toys.remove(toy)
    return redirect('cat-detail', cat_id=cat.id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('cat-index')
        else:
            error_message = "Invalid sign up - try again"

    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)
    # return render(request, 'signup.html',
    #               {
    #                 'form': form,
    #                 'error_message': error_message
    #                }
    #               )