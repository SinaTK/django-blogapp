from django.contrib import admin
from app.models import Post, Profile, Tag, Comments, WebsiteMeta, Vote

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','profile_image', 'bio', 'slug']    
    exclude = ['slug']    

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'count_views'] 
    exclude = ['slug']



class Blogadmin(admin.ModelAdmin):
    admin.site.register(Post, PostAdmin)
    admin.site.register(Profile, ProfileAdmin)
    admin.site.register(Tag)
    admin.site.register(Comments)
    admin.site.register(WebsiteMeta)
    admin.site.register(Vote)