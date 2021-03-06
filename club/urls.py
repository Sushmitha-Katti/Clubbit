"""club URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from club_activities.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('clubs/', show_clubs, name = 'showclubs'),
    path('club/<str:club_name>/', club_page, name = 'club_page1'),
    path('adminlogin/', admin_login , name = "adminlogin"),
    path('see_response/',see_response),  
    path('signin/', signin, name = 'signin'),
    path('signup/', signup, name = 'signup'),
    path('profile/', profile, name = 'profile'),
    path('', home, name = 'name'),
    path ('collegeadmin/', cadmin, name = 'cadmin'),
    path('logout/', signout, name = 'logout'),
    path('add_events/<str:club_name>/',add_events, name = 'adde'),
    path('edit_club/<str:club_name>/',edit_club, name= "edit"),
    path('add_image/<str:club_name>/', addimg, name= "addimg"),
    path('join_requests/<str:club_name>/', joinr, name= "joinr"),
    path("Registered_member/<str:club_name>/",regmem, name = "regmem"),
    path("sel/<str:club_name>/",sel, name = "sel"),
    path("add_admin/<str:club_name>/", add_admin, name = "add_admin"),
    path('club_form/', cform, name = 'cform')



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
