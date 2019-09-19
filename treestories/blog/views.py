from django.db.models import Count, Q 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Post, Author
from .forms import CommentForm, PostForm
from marketting.models import Signup

def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0] 
    return None


def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
          Q(title__icontains=query) |
          Q(overview__icontains=query)   
        )
        context = {
            'queryset' : queryset
        }
        return render(request, 'blog/search_result.html', context)

def get_category_count():
    queryset = Post \
    .objects \
    .values('categories__title') \
    .annotate(Count('categories'))
    return queryset


def index(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]

    if request.method == "POST": 
        email = request.POST["email"]
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()


    context = {
        'object_list': featured,
        'latest' : latest
    }
    return render(request, 'blog/index.html', context)

def blog(request):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 4)
    page_request_var = 'page'
    page= request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'queryset' : paginated_queryset ,
        'most_recent' : most_recent,
        'page_request_var': page_request_var,
        'category_count': category_count
    }
    return render(request, 'blog/blog.html', context)

def post(request, id):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    post = get_object_or_404(Post, id=id)
    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': post.pk
            }))
    context = {
        'form' : form,
        'post' : post,
        'most_recent' : most_recent,
        'category_count': category_count
    }
    return render(request, 'blog/post.html', context)


def post_create(request):
    title = 'Update'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == "POST":
        form.instance.author = author
        if form.is_valid():
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': form.instance.id
            }))
    
    context = {
        'title': title,
        'form': form
    }
    return render(request, "blog/post_create.html", context)

def post_update(request, id):
    title = 'Update'
    post = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, 
    request.FILES or None, 
    instance=post)
    author = get_author(request.user)
    if request.method == "POST":
        form.instance.author = author
        if form.is_valid():
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': form.instance.id
            }))
    
    context = {
        'title': title,
        'form': form
    }
    return render(request, "blog/post_create.html", context)

def post_delete(reqeust, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect(reverse("post-list"))




def magazine(request):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    context = {
        'category_count': category_count,
        'most_recent': most_recent,
    }
    return render(request, 'blog/magazine.html', context )

def contact(request):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    context = {
        'cotegory_count': category_count,
        'most_recent': most_recent,
    }
    return render(request, 'blog/contact.html', context)
