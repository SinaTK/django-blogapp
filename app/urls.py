from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<slug:slug>', views.post_page, name = 'post_page'),
    path('tag/<slug:slug>', views.tag_page, name = 'tag_page'),
    path('author/<slug:slug>/', views.author_page, name = 'author_page'),
    path('search/', views.search_page, name='search_page'),
    path('about', views.about_page, name='about_page'),
    path('all/', views.all_posts, name='all_posts'),
    path('signup/', views.sign_up, name='sign_up'),
    path('login/', views.log_in, name='log_in'),
    path('actionUrl/', views.log_out, name='log_out'),

]
