from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegisterForm, RequestForm, ReviewForm
from .models import Request, Review

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, 'Регистрация прошла успешно! Теперь вы можете войти.')
        return super().form_valid(form)

class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    
    def form_invalid(self, form):
        messages.error(self.request, 'Неверный логин или пароль. Попробуйте еще раз.')
        return super().form_invalid(form)

class ProfileView(LoginRequiredMixin, FormView):
    template_name = 'profile.html'
    form_class = RequestForm
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['requests'] = Request.objects.filter(user=self.request.user).order_by('-created_at')
        
        context['slides'] = [
            'images/slide1.jpg', 'images/slide2.jpg', 
            'images/slide3.jpg', 'images/slide4.jpg'
        ]
        return context

    def form_valid(self, form):
        req = form.save(commit=False)
        req.user = self.request.user
        req.status = 0
        req.save()
        messages.success(self.request, 'Заявка успешно создана!')
        return super().form_valid(form)

class AddReviewView(LoginRequiredMixin, FormView):
    template_name = 'add_review.html'
    form_class = ReviewForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request_obj'] = Request.objects.get(id=self.kwargs['pk'], user=self.request.user)
        return context

    def form_valid(self, form):
        req = Request.objects.get(id=self.kwargs['pk'], user=self.request.user)
        if req.status != 2:
            messages.error(self.request, 'Отзыв можно оставить только после завершения обучения!')
            return redirect('profile')
        
        review = form.save(commit=False)
        review.request = req
        review.save()
        messages.success(self.request, 'Спасибо за отзыв!')
        return redirect('profile')