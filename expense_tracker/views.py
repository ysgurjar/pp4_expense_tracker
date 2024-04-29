from django.shortcuts import render

from django.shortcuts import render, redirect, reverse
from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request,'expense_tracker/home.html')


# Copied code



# Create your views here.

# If user attempts to access page without log in
# redirect to main/base.html
@login_required(login_url="/login")
def user_home(request):
    posts=Post.objects.all()

    if request.method=="POST":
        post_id=request.POST.get("post-id")
        post= Post.objects.filter(id=post_id).first()
        if post and post.author == request.user:
            post.delete()
    
    return render(request,'expense_tracker/home.html', {
        "posts":posts,
    })


def sign_up(request):
    if request.method=="POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect(reverse('home'))
    else:
        form=RegisterForm()

    return render(request,'registration/sign_up.html',{"form":form})