from django.urls import path
from . import views

app_name='movies'

urlpatterns = [
    path('highest/', views.highest, name='highest'),
    path('popularity/', views.popularity, name='popularity'),
    path('search/', views.search, name='search'),
    path('main/', views.main, name='main'),
    path('wishes/', views.wishes, name='wishes'),
    path('evaluate/', views.evaluate, name='evaluate'),
    # path('<int:movie_pk>/scores/<int:score_pk>/show_spoiler', views.show_spoiler, name='show_spoiler'),
    # path('<int:movie_pk>/hate/', views.hate, name='hate'),
    path('<int:movie_pk>/like/', views.like, name='like'),
    path('<int:movie_pk>/scores/<int:score_pk>/update/', views.score_update, name='score_update'),
    path('<int:movie_pk>/scores/<int:score_pk>/delete/', views.score_delete, name='score_delete'),
    path('<int:movie_pk>/scores/new/', views.score_create, name='score_create'),
    # path('<int:movie_pk>/delete/', views.delete, name='delete'),    
    # path('<int:movie_pk>/update/', views.update, name='update'),    
    path('<int:movie_pk>/', views.detail, name='detail'),    
    # path('create', views.create, name='create'),    
    path('list/', views.list, name='list'),    
    path('', views.index, name='index'),    
]