from django.urls import path
from . import views

app_name='posts'

urlpatterns = [
    path('<int:post_pk>/delete/<int:comment_pk>/', views.comment_delete, name='comment_delete'),    
    path('<int:post_pk>/discuss/create/', views.comment_create, name='comment_create'),    
    path('<int:post_pk>/delete/', views.delete, name='delete'),    
    path('<int:post_pk>/update/', views.update, name='update'),    
    path('<int:post_pk>/discuss/', views.detail, name='detail'),    
    path('<int:movie_pk>/create/', views.create, name='create'),    
    path('<int:movie_pk>/', views.index, name='index'),
    # path('', view.list, name='list'),
]