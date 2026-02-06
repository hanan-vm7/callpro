from django.urls import path
from .import views
from .views import add_food_view
 
urlpatterns = [
    path('', views.index, name='index'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('home/',views.home,name='home'),
    path('profile/',views.profile,name='profile'),
    path('logout/',views.logout,name='logout'),
    path('adminlogout/',views.adminlogout,name='adminlogout'),
    path('adminaddfood/',views.adminaddfood,name='adminaddfood'),
    path('editprofile/',views.editprofile,name='editprofile'),
    path('adminlogin/',views.adminlogin,name='adminlogin'),
    path('admindashboard/',views.admindashboard,name='admindashboard'),
    path('adminfoodlist/',views.adminfoodlist,name='adminfoodlist'),
    path('admineditfood/<int:food_id>/',views.admineditfood,name='admineditfood'),
    path("foods/delete/<int:food_id>/", views.admindeletefood, name="admindeletefood"),
    path('userlist/',views.userlist,name='userlist'),
    path('deleteuser/<int:id>',views.deleteuser,name='deleteuser'),
    path("add-food/", add_food_view, name="add_food"),
    path("meals/", views.meals_view, name="meals"),
    path("add-custom-food/", views.add_custom_food, name="add_custom_food"),
    path("delete-meal/<int:id>/", views.delete_meal, name="delete_meal"),
    path('add-favorite/', views.add_favorite_food, name='add_favorite_food'),
    path('report/', views.report_view, name='report'),





  
    
        
    
    
    

]


