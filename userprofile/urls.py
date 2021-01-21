from django.urls import path

from .views import ProfileEditView, ProfileRegisterView, ProfileDetailView, ProfileLoginView, ProfileLogoutView

app_name = 'userprofile'

urlpatterns = [
    path('register', ProfileRegisterView.as_view(), name='register'),
    path('login', ProfileLoginView.as_view(), name='login'),
    path('logout', ProfileLogoutView.as_view(), name='logout'),
    path('<int:pk>', ProfileDetailView.as_view(), name='detail'),
    path('<int:pk>/edit', ProfileEditView.as_view(), name='edit')
]
