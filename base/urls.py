##The ids come from the admin page that are the number given to users,rooms or any other things associated with it.

from django.contrib import admin
from django.urls import URLPattern, path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),        # so we give the url a name so that we will use that name anywhere and 
                                                            ## whenever we need to change the url we dont need to change it every file 
                                                            ### where we used it as we have used its name only, so name here is working
                                                            ## as a variable.
    path('create-room/', views.Createroom, name="create-room"),
    path('update-room/<str:pk>/', views.Updateroom, name="update-room"),
    path('user-profile/<str:pk>/',views.Userprofile, name="user-profile"),
    path('delete-room/<str:pk>/', views.Deleteroom, name="delete-room"),
    path('login/',views.Loginpage, name="login"),
    path('register/',views.Registerpage, name="register"),
    path('logout/',views.Logoutuser, name="logout"),
    path('delete-message/<str:pk>/', views.Deletemessage, name="delete-message"),
    path('update-user/', views.Updateuser, name="update-user"),
    path('topics/', views.Topicspage, name="topics"),
    path('activity/', views.Activitypage, name='activity')
]

