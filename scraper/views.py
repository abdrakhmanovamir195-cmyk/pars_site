from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Site, ParseTask, Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login



def index(request):
    try:
        categories = Category.objects.all().select_related('site')
    except Exception as e:
        categories = []
    return render(request, 'index.html', {'categories': categories})


def start_parsing(request):
    if request.method == 'POST':
        selected_categories = request.POST.getlist('categories')

        task = ParseTask.objects.create(user=request.user, status='pending')
        task.categories.set(selected_categories)

        for cat_id in selected_categories:
            category = Category.objects.get(id=cat_id)
            if hasattr(category, 'site') and category.site:
                task.sites.add(category.site)
                from .tasks import run_parser
                run_parser.delay(task.id, category.site.parser_key)

        task.save()
        return redirect('results', task_id=task.id)

    return redirect('index')


def results(request, task_id):
    task = get_object_or_404(ParseTask, id=task_id, user=request.user)
    products = Product.objects.filter(task=task)

    sort = request.GET.get('sort', '')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'name_asc':
        products = products.order_by('name')
    elif sort == 'name_desc':
        products = products.order_by('-name')

    return render(request, 'results.html', {
        'task': task,
        'products': products,
    })

