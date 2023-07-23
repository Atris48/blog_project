import datetime
from random import randint
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from account_app.forms import UserCreationForm, UserEditProfile
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from account_app.models import User

user = User.objects.first()
user.email = ''


class SignupView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = UserCreationForm()
        return render(request, 'account_app/signup.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = UserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            confirm_password = request.POST.get('password2')
            if password != confirm_password:
                messages.error(request, 'پسوورد و تایید پسوورد مشابه نمیباشد')
                return redirect('signup')
            verification_code = randint(1000, 9999)
            request.session['verify_code'] = verification_code
            request.session['email'] = email
            request.session['code_timestamp'] = datetime.datetime.now().timestamp()
            email = EmailMessage(
                'blog.mmd',
                f'کد فعال سازی اکانت شما: {verification_code} میباشد ',
                'seyedmamad86@gmail.com',
                (email,),
            )
            email.send()
            user = User.objects.create(email=email)
            user.set_password(password)
            user.is_active = False
            user.save()
            return redirect('verify_email')
        return render(request, 'account_app/signup.html', {'form': form})


class VerifyEmailView(View):

    def get(self, request):
        return render(request, 'account_app/verify_email.html')

    def post(self, request):
        code = request.POST.get('code')
        user = User.objects.get(email=request.session['email'])
        code_timestamp = request.session.get('code_timestamp')
        if code and code_timestamp:
            current_timestamp = datetime.datetime.now().timestamp()
            expiration_duration = datetime.timedelta(hours=6).total_seconds()

            if current_timestamp - code_timestamp > expiration_duration:
                # Code has expired
                messages.error(request, 'کد تایید شما منقضی شده است، کد جدید دریافت کنید')
                return redirect('resend_code')
        if int(code) == int(request.session['verify_code']):
            user.is_active = True
            user.save()
            messages.success(request, 'اکانت شما با موفقیت فعال شد')
            return redirect('login')
        else:
            return render(request, 'account_app/verify_email.html', {'error': 'Invalid verification code'})


def resend_code(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user.is_active:
            messages.error(request, 'اکانت شما تایید شده است')
            return redirect('home')
        else:
            verification_code = randint(1000, 9999)
            user.code = verification_code
            user.save()
            email = EmailMessage(
                'blog.mmd',
                f'کد فعال سازی اکانت شما: {verification_code} میباشد ',
                'seyedmamad86@gmail.com',
                (email,),
            )
            email.send()
            messages.success(request, 'ایمیل حاوی کد تایید برای شما ارسال شد')
            return redirect('verify_email')
    else:
        return render(request, 'account_app/resend_code.html')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pass')
        user = User.objects.filter(email=email).first()
        if user.is_active:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'کاربری یافت نشد')
                return redirect('login')
        else:
            messages.error(request, 'شما باید اکانت خود را فعال کنید')
            return redirect('verify_email')
    else:

        return render(request, 'account_app/login.html')


def user_logout(request):
    logout(request)
    return redirect('home')


def user_edit_profile(request):
    if not request.user.is_authenticated:
        messages.error(request, 'وارد شوید')
        return redirect('login')
    if request.method == 'POST':
        form = UserEditProfile(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_edit_profile')
    form = UserEditProfile(instance=request.user)
    return render(request, 'account_app/edit_profile.html', {'form': form})
