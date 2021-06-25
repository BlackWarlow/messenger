from django.shortcuts import render
from django.views import View
from main.forms import *
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.urls import reverse
# Create your views here.


class index_page(View):
    def get(self, request):
        context = {'user': request.user}
        return render(request, 'pages/index.html',context)


class login_page(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index_page')
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


class register_page(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index_page')
        context = {'form': RegisterForm()}
        return render(request, 'pages/register.html', context)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.save(request):
            return redirect('index_page')
        else:
            context = {'form': form}
            return render(request, 'pages/register.html', context)


class profile_page(View):
    def get(self, request, username=None):
        if username == None or username == request.user.username:
            if request.user.is_authenticated:
                form = SearchProfileForm()
                profile = Profile.objects.filter(user=request.user).first()
                context = {'user': request.user, 'profile': profile, 'form': form}
                return render(request, 'pages/profile.html', context)
            return redirect('index_page')
        else:
            context = {'page_title': 'Профиль'}

            u = User.objects.filter(username=username).first()
            if u != None:
                context['page_title'] += ' ' + u.username
                context['p_user'] = u

                p = Profile.objects.filter(user=u).first()
                if p != None:
                    context['profile'] = p

                    if request.user.is_authenticated:
                        p_current = Profile.objects.filter(user=request.user).first()

                        d1 = Dialog.objects.filter(sender=p, reciever=p_current).first()
                        d2 = Dialog.objects.filter(sender=p_current, reciever=p).first()

                        d = None
                        if d1 != None:
                            d = d1
                        elif d2 != None:
                            d = d2

                            if d != None:
                                context['dialog'] = d

                return render(request, 'pages/user_profile.html', context)
            else:
                return redirect('index_page')

    def post(self, request, username=None):
        if username == None or username == request.user.username:
            form = SearchProfileForm(request.POST)
            result = form.search(request)
            context = {'form': form, 'result': result}
            return render(request, 'pages/search_profile.html', context)
        return redirect('my_profile_page')


class profile_search(View):
    def get(self, request, search_str=None):
        if search_str != None:
           form = SearchProfileForm(initial={'search_str': search_str})
        else:
           form = SearchProfileForm()
           
        context = {'form': form}
        return render(request, 'pages/search_profile.html', context)

    def post(self, request, search_str=None):
        form = SearchProfileForm(request.POST)
        result = form.search(request)
        context = {'form': form, 'result': result}
        return render(request, 'pages/search_profile.html', context)


class all_dialogs(View):
    def get(self, request):
        context = dict()
        if request.user.is_authenticated:
            p = Profile.objects.filter(user=request.user).first()
            if p != None:
                dialogs = []

                for d in list(Dialog.objects.filter(sender=p)):
                    dialogs.append(d)
                for d in list(Dialog.objects.filter(reciever=p)):
                    dialogs.append(d)

                context.update({'profile': p, 'dialogs': dialogs})

            return render(request, 'pages/my_dialogs.html', context)
        else:
            return redirect('index_page')

class create_dialog(View):
    def get(self,request,username=None):
        if username == None:
            return redirect('index_page')

        u = User.objects.filter(username=username).first()
        if u == None:
            return redirect('index_page')

        if request.user.is_authenticated:
            p = Profile.objects.filter(user=request.user).first()

            p_u = Profile.objects.filter(user=u).first()
            if p != None and p_u != None:
            # Код программы

                d1 = Dialog.objects.filter(sender=p, reciever=p_u).first()
                d2 = Dialog.objects.filter(reciever=p_u, sender=p).first()
                if d1 == None and d2 == None:
                    form = NewDialogForm()
                    context = {'form': form, 'user_profile': p_u}
                    return render(request, 'pages/new_dialog.html', context)
                else:
                    return redirect('my_dialogs')
            else:
                return redirect('my_profile_page')
        else:
            return redirect('login_page')

    def post(self, request, username=None):
        if username == None:
            return redirect('index_page')

        u = User.objects.filter(username=username).first()
        if u == None:
            return redirect('index_page')

        if request.user.is_authenticated:
            p = Profile.objects.filter(user=request.user).first()

            p_u = Profile.objects.filter(user=u).first()
            if p != None and p_u != None:
                # Код программы

                d1 = Dialog.objects.filter(sender=p, reciever=p_u).first()
                d2 = Dialog.objects.filter(reciever=p_u, sender=p).first()
                if d1 == None and d2 == None:
                    form = NewDialogForm(request.POST)
                    result, d = form.save(request, p, p_u)
                    if result:
                        return redirect(reverse('dialog', args=[d.link]))
                    context = {'form': form, 'user_profile': p_u}
                    return render(request, 'pages/new_dialog.html', context)
                else:
                    return redirect('my_dialogs')
            else:
                return redirect('my_profile_page')
        else:
            return redirect('login_page')

class dialog_page(View):
    def get(self,request,link = None):
        if not request.user.is_authenticated:
            return redirect('login_page')

        if link == None:
            return redirect('my_dialogs')

        d = Dialog.objects.filter(link=link).first()
        if d == None:
            return redirect('my_dialogs')

        context = {'d': d}
        return render(request, 'pages/dialog.html', context)

