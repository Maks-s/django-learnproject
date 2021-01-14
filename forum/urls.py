from django.urls import include, path

from .views import PostCreateView, PostListView, PostDetailView

app_name = 'forum'

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('new', PostCreateView.as_view(), name='post-create'),
    path('p/<int:pk>', PostDetailView.as_view(), name='post-detail')
]
