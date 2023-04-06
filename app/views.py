import time
from django.shortcuts import render
from app.models import BlogUser, Comments, Post, Profile, Tag, WebsiteMeta
from app.forms import CommentForm, LogInForm, SignInForm, SignUpForm, SubscribeForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count

# Create your views here.
def index(request):
    subscribe_form = SubscribeForm()
    posts = Post.objects.all()
    top_blogs = posts.order_by('-count_views')[0:3]
    new_blogs = posts.order_by('-last_update')[0:3]
    subscribe_successful = None
    feature_blog = Post.objects.filter(is_featured=True)
    website_info = None

    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]
        
    if feature_blog:
        feature_blog = feature_blog[0]

    if request.POST:
        subscribe = SubscribeForm(request.POST)
        if subscribe.is_valid:
            subscribe.save()
            subscribe_successful = 'subscribe_successfully'
            subscribe_form = SubscribeForm() 
            # return HttpResponseRedirect(reverse('index'))

    context = {'posts': posts, 'top_blogs': top_blogs, 'new_blogs': new_blogs, 'subscribe_form': subscribe_form,
               'subscribe_successful': subscribe_successful, 'feature_blog': feature_blog, 'website_info': website_info,
               'count': '-count_views'}
    return render(request, 'app/index.html', context)

def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    comments = Comments.objects.filter(post=post, parent=None)
    form = CommentForm()
    new_posts = Post.objects.order_by('-last_update')[0:3]
    top_posts = Post.objects.order_by('count_views')[0:3]
    tags = Tag.objects.all()[0:15]
    # catch other post of this author exclude this post
    author_posts = Post.objects.filter(author=post.author).exclude(slug=slug).order_by('-count_views')[0:2]

    if request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            parent_obj = None
            if request.POST.get('parent'):
                # save reply
                parent = request.POST.get('parent')
                parent_obj = Comments.objects.get(id=parent)
                if parent_obj:
                    reply_comment = comment_form.save(commit=False)              
                    reply_comment.parent = parent_obj
                    reply_comment.post = post
                    reply_comment.save()
                    return HttpResponseRedirect(reverse('post_page', kwargs={'slug': slug}))

            else:
                comment = comment_form.save(commit=False)
                postid = request.POST.get('post_id')
                post = Post.objects.get(id=postid)
                comment.post = post
                comment.save()
                return HttpResponseRedirect(reverse('post_page', kwargs={'slug': slug}))
    
    if not post.count_views:
        post.count_views = 1
    else:
        post.count_views += 1
    post.save()

    context = {'post':post, 'form': form, 'comments': comments, 'new_posts': new_posts,
                'top_posts':top_posts, 'tags':tags, 'author_posts': author_posts}
    return render(request, 'app/post.html', context)

def tag_page(request, slug):
    tags = Tag.objects.all()
    tag = Tag.objects.get(slug=slug)
    posts = tag.post.all()
    top_posts = posts.order_by('-count_views')[0:2]
    # top_posts = Post.objects.filter(tags__in=[tag.id]).order_by('-count_views')[0:2]
    new_posts = posts.order_by('-last_update')[0:3]
    # new_posts = Post.objects.filter(tags__in=[tag.id]).order_by('-last_update')[0:3]

    context ={'tag': tag, 'tags': tags, 'top_posts': top_posts, 'new_posts': new_posts}

    return render(request, 'app/tag.html', context)

def author_page(request, slug):
    profile = Profile.objects.get(slug=slug)
    top_posts = Post.objects.filter(author=profile.user).order_by('-count_views')[0:2]
    new_posts = Post.objects.filter(author=profile.user).order_by('-last_update')[0:3]
    top_authors = User.objects.annotate(number=Count('post')).order_by('-number')
    

    context = {'profile': profile, 'top_authors': top_authors, 'top_posts': top_posts,'new_posts': new_posts}
    return render(request, 'app/author.html', context)

def search_page(request):
    search_query = ''
    posts = []
    if request.GET.get('q'):
        search_query = request.GET.get('q')
        posts = Post.objects.filter(title__icontains=search_query)


    context = {'posts':posts, 'search_query':search_query}
    return render(request, 'app/search.html', context)

def about_page(request):
    website_info = None
    request.session['log_in'] = False
    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]

    context = {'website_info': website_info}
    return render(request, 'app/about.html', context)

def all_posts(request):
    order = request.GET.get('order', '-count_views')    # create a query parameter with a default value
    tag_name = request.GET.get('tag', '')
    posts = Post.objects.all().order_by(order)
    if tag_name:
        tag = Tag.objects.get(name=tag_name)
        posts = Post.objects.filter(tags__in=[tag.id])

    context = {'posts': posts}
    return render(request, 'app/allposts.html', context)

def log_in_user(request, username: str):
    request.session['log_in'] = True    
    request.session['username'] = username

def log_out(request):
    request.session['log_in'] = False
    messages.success(request, 'You log out successfully', extra_tags='success-message')
    return HttpResponseRedirect(reverse('index'))



def sign_up(request):
    form = SignInForm()
    error_message = ""
    if request.POST:
        signup = SignInForm(request.POST)
        if signup.is_valid():
            if signup.cleaned_data['password'] == signup.cleaned_data['password_2']:
                signup.save()
                username = signup.cleaned_data['user_name']
                log_in_user(request, username)       
                return HttpResponseRedirect(reverse('index'))
            else:
                error_message = "Password and it's repeat not same"  
        else:
            error_message =  'Unsuccessful Registration, Invalid inforamtion'

    context = {'form':form, 'error_message':error_message}
    return render(request, 'app/signup.html', context)

def log_in(request):
    form = LogInForm()
    error_message = ''
    if request.POST:  
        login = LogInForm(request.POST)  
        if login.is_valid():  
            username = login.cleaned_data['user_name']
            pas = login.cleaned_data['password']
            try:
                BlogUser.objects.get(user_name=username)
                user = BlogUser.objects.get(user_name=username)
                if user.password == pas:
                    # messages.success(request, 'Form submission successful')
                    log_in_user(request, username)
                    messages.success(request, 'You log in successfully', extra_tags='learn')
                    return HttpResponseRedirect(reverse('index'))
                else:
                    error_message = 'incorrect password'
            except:
                error_message ='username not found'

    context = {'form': form, 'error_message':error_message}
    return render(request, 'app/login.html', context)


