from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.http import HttpResponse

import textract, re


from .forms import LoginForm, SignUpForm


# Create your views here.
class SignUpView(FormView):
    template_name = 'signup.html'
    form_class = SignUpForm

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user and user.is_authenticated:
            return redirect('assign1:dashboard')

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        user.refresh_from_db()
        user.profile.user_registration_file = form.cleaned_data.get('user_registration_file')
        user.save()
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=user.username, password=raw_password)
        if not user:
            return HttpResponse("Username or Password is incorrect...")

        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return "%s" % (next_url)
        else:
            return reverse_lazy('index')

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user and user.is_authenticated:
            return redirect('assign1:dashboard')
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return "%s" % (next_url)
        else:
            return reverse_lazy('index')

    def form_invalid(self, form):
        #  print(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
        if not user.is_authenticated:
            return HttpResponse("Username or Password is incorrect...")

        login(self.request, user)
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        file = request.user.profile.user_registration_file
        text = textract.process(file.path).decode('utf-8')
        words = re.findall(r"[^\W_]+", text, re.MULTILINE)
        word_cnt = len(words)
        ctx = {
            'word_cnt': word_cnt,
        }
        return render(request=request, template_name='dashboard.html', context=ctx)

@method_decorator(login_required, name='dispatch')
class Assign1IndexView(TemplateView):
    template_name = 'assign1_index.html'
