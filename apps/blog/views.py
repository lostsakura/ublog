from django.shortcuts import render

# Create your views here.


def blog_index(request):
    return render(request, 'index.html')


def blog_admin(request):
    return render(request, 'admin.html')
