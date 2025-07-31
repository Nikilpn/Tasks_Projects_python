from django.shortcuts import render
from blogapp.models import Blog

# Create your views here.

# def index_page(request):
#     qs=Blog.objects.all()
#     return render(request,"index.html")
def index_page(request):
    blogs = Blog.objects.all().select_related('owner')  # Get all blogs with owner info
    return render(request, "index.html", {'blogs': blogs})