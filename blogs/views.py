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
                'url': 'blog_detail/{}/'.format(blog.id),  # Optional: Add a URL for event click
            })
        except Exception as e:
            print(f"Error processing blog {blog.id}: {e}")

    # Return events as JSON response
    return JsonResponse(events, safe=False)
    

@login_required
def get_blog_data(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)

    if request.method == 'POST':
        # Update the blog post with the submitted data
        blog.title = request.POST.get('title', '')
        blog.author = request.POST.get('author', '')
        blog.date = datetime.datetime.strptime(request.POST.get('date', ''), '%Y-%m-%d')
        blog.content = request.POST.get('content', '')
        blog.save()

        return JsonResponse({'status': 'success'})
    else:
        # Return the current blog data for editing
        data = {
            'title': blog.title,
            'author': blog.author,
            'date': blog.date.strftime('%Y-%m-%d'),
            'content': blog.content,
        }
        return JsonResponse(data)

@login_required
def delete_post(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    blog.delete()
    return redirect('blogs:home')



@login_required
def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'blogPost.html', {'blog': blog})


@login_required
def get_user_name(request):
    user = request.user
    data = {
        'user': user.username
    }
    return JsonResponse(data)




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

def editPost(request, blog_id):
    # Retrieve the existing blog post based on blog_id
    blog_post = get_object_or_404(Blog, pk=blog_id)

    if request.method == "POST":
        # Populate the form with the existing blog post data
        form = BlogForm(request.POST, instance=blog_post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.username
            post.save()
            return redirect('blogs:home')
        print(form.errors)
    else:
        # Populate the form with the existing blog post data
        form = BlogForm(instance=blog_post)

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
