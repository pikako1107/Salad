from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from . import forms

# Create your views here.

# ログインクラス
class MyLoginView(LoginView):
    form_class = forms.LoginForm
    template_name = "appManagement/login.html"

# ログアウトクラス
class MyLogoutView(LoginRequiredMixin, LogoutView):
    template_name = "appManagement/logout.html"

# メインページ表示
@login_required
def index(request):

    # ページURL
    goto = ('products', 'sets', 'sales')

    params = {
            'title':'さらぼー管理ツール',
            'goto':goto
        }
    return render(request, 'appManagement/index.html', params)
