from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('',                       views.PostListView.as_view(),    name='list'),
    path('<slug:slug>/',            views.PostDetailView.as_view(),  name='detail'),
    path('<slug:slug>/like/',       views.LikeToggleView.as_view(),  name='like'),
    path('<slug:slug>/comment/',    views.CommentCreateView.as_view(), name='comment'),
]
