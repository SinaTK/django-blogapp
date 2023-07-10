from django.shortcuts import render, get_object_or_404, redirect
from app.models import Comments, Post, Profile, Tag, Vote, WebsiteMeta
from app.forms import CommentForm, SubscribeForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Count, QuerySet
from django.db.models import QuerySet as Q
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


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
    comments_count = comments.count()
    form = CommentForm()
    new_posts = Post.objects.order_by('-last_update')[0:3]
    top_posts = Post.objects.order_by('count_views')[0:3]
    tags = Tag.objects.all()[0:15]
    likes = post.pvote.count()
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
                    return HttpResponseRedirect(reverse('home:post_page', kwargs={'slug': slug}))

            else:
                comment = comment_form.save(commit=False)
                postid = request.POST.get('post_id')
                post = Post.objects.get(id=postid)
                comment.post = post
                comment.save()
                return HttpResponseRedirect(reverse('home:post_page', kwargs={'slug': slug}))
    
    if not post.count_views:
        post.count_views = 1
    else:
        post.count_views += 1
    post.save()

    context = {'post':post, 'form': form, 'comments': comments,'comments_count': comments_count, 'new_posts': new_posts,
                'top_posts':top_posts, 'tags':tags, 'author_posts': author_posts, 'likes':likes}
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
    other_authors = Profile.objects.exclude(user=profile.user)
    

    context = {'profile': profile, 'other_authors': other_authors, 'top_posts': top_posts,'new_posts': new_posts}
    return render(request, 'app/author.html', context)

def search_page(request):
    search_query = ''
    posts = []
    if request.GET.get('q'):
        search_query = request.GET.get('q')
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(title__icontains=search_query))


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

class LikePostView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        user = request.user
        post = get_object_or_404(Post, pk=post_id)
        if Vote.objects.filter(user=user, post=post).exists():
            messages.error(request, 'You already like this post.')
        else:
            Vote.objects.create(user=user, post=post)

        return redirect('home:post_page', post.slug)