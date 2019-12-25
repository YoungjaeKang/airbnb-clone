from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms


class LoginView(FormView):
    """ Full Django Login """
    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")
    # initial = {
    #     'email': "hyunjin@naver.com"
    # }

    def form_valid(self, form):
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(self.request, username=email, password=password)
            if user is not None:
                login(self.request, user)
            return super().form_valid(form)


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    initial = {
        'first_name': 'Nicolas',
        'last_name': 'Serr',
        'email': 'itn@las.com',
    }

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)



""" # 직접 만들어본 로그인 뷰
class LoginView(View):
    def get(self, request):
        form = forms.LoginForm()
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("core:home"))

        return render(request, "users/login.html", {"form": form})
""" 

# def login_view(request):
#     if request.method == "GET":
#         pass
#     elif request.method == "P"