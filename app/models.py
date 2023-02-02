from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
# from django.utils.crypto import get_random_string

# Create your models here.
class Subscribe(models.Model):
    email = models.EmailField(max_length=100)
    date = models.DateTimeField(auto_now=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='images/', null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True)
    bio = models.CharField(max_length=200)
    
    def __str__(self):
        return self.user.first_name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.user.username)
        return super(Profile, self).save(*args, **kwargs)

        # if not self.id:
            # if self.name not in self.objects.all():
            #     self.slug = slugify(self.name)
            # else:
            # self.slug = slugify(self.name + '-' + get_random_string(4))
        

class Tag(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        return super(Tag, self). save(*args, **kwargs)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    last_update = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True, auto_created=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='post')
    count_views = models.IntegerField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        return super(Post, self). save(*args, **kwargs)

class Comments(models.Model):
    content = models.TextField()
    date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    website = models.CharField(max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    auhtor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey("self", on_delete=models.DO_NOTHING, null=True, blank=True, related_name='replies')

class WebsiteMeta(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    about = models.TextField()


class BlogUser(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    user_name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=254)
    date = models.DateTimeField(auto_now=True)
    password = models.CharField(max_length=50)
    password_2 = models.CharField(max_length=50)

    

   