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
    success_url = reverse_lazy('assign1:dashboard')

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user and user.is_authenticated:
            return redirect('assign1:dashboard')

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        user.refresh_from_db()  # load the profile instance created by the signal
        # user.profile.birth_date = form.cleaned_data.get('birth_date')
        user.profile.user_registration_file = form.cleaned_data.get('user_registration_file')
        # import ipdb ; ipdb.set_trace()
        # print(form.cleaned_data)
        user.save()
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=user.username, password=raw_password)
        if not user:
            return HttpResponse("Username or Password is incorrect...")

        login(self.request, user)
        return super().form_valid(form)


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('assign1:dashboard')

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user and user.is_authenticated:
            return redirect('assign1:dashboard')
        return super().get(request, *args, **kwargs)

    # def get_context_data(self, **kwargs):
    #     ctx = super().get_context_data(**kwargs)
    #     # ctx['for']
    #     return ctx

    def form_invalid(self, form):
        #  print(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
        if not user.is_authenticated:
            return HttpResponse("Username or Password is incorrect...")

        login(self.request, user)
        return super().form_valid(form)

class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        # profile = request.user.profile
        file = request.user.profile.user_registration_file
        # print(profile.get_user_registration_file_name())
        # import ipdb ; ipdb.set_trace()
        text = textract.process(file.path).decode('utf-8') # http://www.africau.edu/images/default/sample.pdf
        # text = textract.process('sample.pdf') # http://www.africau.edu/images/default/sample.pdf
        # print(text)
        words = re.findall(r"[^\W_]+", text, re.MULTILINE) # regex demo and explanation - https://regex101.com/r/U7WMSA/1
        word_cnt = len(words)
        ctx = {
            'word_cnt': word_cnt,
            # 'profile': profile
        }
        return render(request=request, template_name='dashboard.html', context=ctx)

class Assign1IndexView(TemplateView):
    template_name = 'assign1_index.html'
