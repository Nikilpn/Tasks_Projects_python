from django.urls import path
from blogapp.views import RegisterApiView,UserLoginApiView,AddBlogApiView,ListAllBlog,BlogUpdateApiView,DeleteBlogApiView,ReportBlogApiView,GetReportListView

urlpatterns = [
    path('register/',RegisterApiView.as_view(),name='register_new_user'),
    path('login/',UserLoginApiView.as_view(),name='userlogin'),
    path('blog-create',AddBlogApiView.as_view(),name='blog-create'),
    path('blog-list',ListAllBlog.as_view(),name='blog-list'),
    path('blog-update/<int:pk>/',BlogUpdateApiView.as_view(),name='blog-update'),
    path('blog-delete/<int:pk>/',DeleteBlogApiView.as_view(),name='blog-delete'),
    
    #blacklist
    path('blog-Report/',ReportBlogApiView.as_view(),name='blog-Report'),
    path('blog-report-list/',GetReportListView.as_view(),name='blog-report-list'),
    
    
 
]
