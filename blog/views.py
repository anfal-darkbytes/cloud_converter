from django.http import JsonResponse
from django.shortcuts import render
from .models import BlogModel
from django.shortcuts import get_object_or_404


def blog(request):
    blog_list = BlogModel.objects.all()

    return render(request, 'blog/blog.html', {'blog_list': blog_list})

def blog_by_id(request, slug):
    blog_obj = get_object_or_404(BlogModel, slug=slug)
    return render(request, 'blog/blog_by_id.html', {'blog_obj':blog_obj})

def search_by_query(request):
    print(f'========================>>>{request.method == 'POST'}')
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        print(f'========================>>>{request.POST.get('search_query')}')
        filter_blog = BlogModel.objects.filter(heading__icontains=search_query)
        print(f'========================>>>{filter_blog}')
        return render(request, 'blog/search.html', {'filter_blog': filter_blog})

    return JsonResponse({
        'success': False,
        'message': 'Invalid request',
    })
