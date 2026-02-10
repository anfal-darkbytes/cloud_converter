from django.shortcuts import render
from blog.models import BlogModel, CategoryModel
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q


def blog(request):
    categories = CategoryModel.objects.all()
    if request.method == 'GET':

        category_query = request.GET.get('category', '')
        filtered_blog = BlogModel.objects.filter(category__name__icontains=category_query)

        paginator = Paginator(filtered_blog, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'blog/blog.html', {'blog_list': page_obj, 'categories': categories})

    blog_list = BlogModel.objects.select_related()

    paginator = Paginator(blog_list, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/blog.html', {'blog_list': page_obj, 'categories': categories})

def blog_by_id(request, slug):

    blog_obj = get_object_or_404(BlogModel, slug=slug)
    return render(request, 'blog/blog_by_id.html', {'blog_obj':blog_obj})


def search_by_query(request):
    search_query = request.GET.get('q', '')
    filter_blog = BlogModel.objects.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query) |
    Q(author__icontains=search_query) | Q(hash_tag__icontains=search_query))

    return render(request, 'blog/search.html', {
        'filter_blog': filter_blog,
        'query': search_query,
    })

