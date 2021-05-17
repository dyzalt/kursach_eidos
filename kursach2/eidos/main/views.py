from django.shortcuts import render, redirect
from .models import Articles
from .forms import ArticlesForm
from django.views.generic import DetailView

def index(request):
    news = Articles.objects.order_by('-date')
    return render(request, 'main/index.html', {'news': news})

def create(request):
    error = ''
    if request.method == 'POST':
        form = ArticlesForm(request.POST, request.FILES)
        if form:
            form.save()
            return redirect('home')
        else:
            error = 'Form was false'
    form = ArticlesForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'main/create.html', data)

class NewsDetailWiew(DetailView):
    model = Articles
    template_name = 'main/detail_view.html'
    context_object_name = 'article'
