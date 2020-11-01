from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('index/',views.index,name='index'),
    path('jobs/',views.jobs,name=''),
    path('candidate/',views.candidate,name='candidate'),
    path('contact/',views.contact,name='contact'),
    path('job_details/',views.job_details,name='job_details'),
    path('blog/',views.blog,name='blog'),
    path('single-blog/',views.single_blog,name='single-blog'),
    path('login/',views.login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('register/',views.register,name='register'),
    path('validate/',views.validate,name='validate'),
    path('logout/',views.logout,name='logout'),
    path('post-job/',views.post_job,name='post-job'),
    path('add-job/',views.add_job,name='add-job'),
    path('apply/',views.apply,name='apply')

]