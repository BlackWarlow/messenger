from django.shortcuts import render
from django.views import View
from main.forms import *
from django.shortcuts import redirect
from django.contrib.auth import logout
# Create your views here.
class index_page(View):
    def get(self, request):
        context = {'user': request.user}
        return render(request, 'pages/index.html',context)


class login_page(View):
    def get(self, request):
        context = {'form': AuthForm()}
        return render(request, 'pages/login.html', context)

    def post(self, request):
        form = AuthForm(request.POST)
        if form.save(request):
            return redirect('index_page')
        else:
            context = {'form': form}
            return render(request, 'pages/login.html', context)


class logout_page(View):
    def get(self, request):
        logout(request)
        return redirect('index_page')

    def post(self, request):
        logout(request)
        return redirect('index_page')