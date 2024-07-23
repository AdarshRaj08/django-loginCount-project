from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.cache import cache

# Create your views here.


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)

            # logincount
            name = user.username
            mv = cache.get_or_set(name,0,80000)
            mv = cache.incr(name,delta=1)
            return render(request,'project/profile.html',{'form':form,'count':mv})
    else:
        form = UserCreationForm()
    return render(request,'project/signup.html',{'form':form})


def login_view(request):
    if request.method == 'POST':
        print("----------------------")
        print("after post ")
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            print("inside valid ",username)
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                # logincount
                name = user.username
                mv = cache.get_or_set(name,0,80000)
                mv = cache.incr(name,delta=1)
                return render(request,'project/profile.html',{'form':form,'count':mv})
    else:
        form = AuthenticationForm()
    return render(request, 'project/login.html', {'form': form})



# profile

@login_required
def profile(request):
    return render(request,'project/profile.html')

