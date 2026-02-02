from django.shortcuts import render
from .models import BlogModel, CategoryModel
from django.shortcuts import get_object_or_404


def blog(request):
    blog_list = BlogModel.objects.all()
    categories = CategoryModel.objects.all()

    return render(request, 'blog/blog.html', {'blog_list': blog_list, 'categories':categories})

def blog_by_id(request, slug):
    blog_obj = get_object_or_404(BlogModel, slug=slug)
    return render(request, 'blog/blog_by_id.html', {'blog_obj':blog_obj})


def search_by_query(request):
    search_query = request.GET.get('search_query', '')
    filter_blog = BlogModel.objects.filter(title__icontains=search_query)


    return render(request, 'blog/search.html', {
        'filter_blog': filter_blog,
        'query': search_query,

    })