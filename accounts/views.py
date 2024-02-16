from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm

# Create your views here.
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request,
                                username=data['username'],
                                password=data['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Successfully logined')
                else:
                    return HttpResponse('Your profile is not active')
            else:
                return HttpResponse('Username and password is not correct')
    else:
        form = LoginForm()
        context = {
            'form': form
        }

    return render(request, 'account/login.html', context)


def dashboard_view(request):
    user = request.user

    context = {
        "user": user,
        }

    return render(request, 'pages/user_profile.html', context)