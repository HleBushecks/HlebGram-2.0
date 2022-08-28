"""HlebGram_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from HlebGram import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.startpage, name='startpage'),
    path('login/', views.loginpage, name='loginpage'),
    path('signup/', views.signuppage, name='signuppage'),
    path('logout/', views.logoutpage, name='logoutpage'),
    path('home/', views.homepage, name='homepage'),
    path('profile/', views.profilepage, name='profilepage'),
    path('change/', views.changepage, name='changepage'),
    path('user/<int:user_pk>/', views.userpage, name='userpage'),
    path('user/<int:user_pk>/subscribers', views.subscriberspage, name='subscriberspage'),
    path('user/<int:user_pk>/subscriptions', views.subscriptionspage, name='subscriptionspage'),
    path('search', views.searchpage, name='searchpage'),
    path('add-photo', views.addphotopage, name='addphotopage'),
    path('photo/<int:pk>/', views.photopage, name='photopage'),
    path('delete', views.deletepage, name='deletepage')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
