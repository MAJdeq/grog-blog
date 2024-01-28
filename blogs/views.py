from datetime import date, datetime
from time import strftime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from blogs.forms import BlogForm
from .models import Blog, Comments
from django.contrib.staticfiles import finders
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.utils.safestring import mark_safe
from django.core.serializers import serialize


@login_required
def get_blogs(request):
    blogs = Blog.objects.all()

    # Convert blog data to FullCalendar events
    events = []
    for blog in blogs:
        try:
            formatted_date = blog.date.strftime('%Y-%m-%d')
            events.append({
                'title': blog.title,
                'start': formatted_date,  # Format date in 'YYYY-MM-DD'
                'url': 'blog/detail/{}/'.format(blog.id),  # Optional: Add a URL for event click
            })
        except Exception as e:
            print(f"Error processing blog {blog.id}: {e}")

    # Return events as JSON response
    return JsonResponse(events, safe=False)



@login_required
def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'blogPost.html', {'blog': blog})



@login_required
def index(request):
    blogList = Blog.objects.order_by('-date')
    time = strftime('%c')
    
    return render(request, "home.html", {'time': time, 'blogs': blogList})

@login_required
def newPost(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blogs:home')
        print(form.errors)
    else:
        form = BlogForm()
    return render(request, 'home.html', {'form': form})


def custom_css(request):
    css_path = finders.find('blogs/style.css')

    if css_path:
        with open(css_path, 'r') as css_file:
            css_content = css_file.read()

        response = HttpResponse(css_content, content_type='text/css')
        return response
    else:
        return HttpResponse(status=404)
