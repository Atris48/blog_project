from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from contact_us_app.models import Contact_us
from .forms import CaptchaTestForm
from django.contrib import messages


@csrf_exempt
def contact_us(request):
    form = CaptchaTestForm()
    if request.method == 'POST':
        form = CaptchaTestForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name')
            if name == None or name == '':
                messages.error(request, 'نام خود را وارد کنید')
                return redirect('contact_us')
            email = request.POST.get('email')
            if email == None or email == '':
                messages.error(request, 'ایمیل خود را وارد کنید')
                return redirect('contact_us')
            phone = request.POST.get('phone')
            if phone == None or phone == '':
                messages.error(request, 'شماره ی خود را وارد کنید')
                return redirect('contact_us')
            if not phone.isnumeric():
                messages.error(request, 'شماره باید عدد باشد')
                return redirect('contact_us')
            message = request.POST.get('message')
            if message == None or message == '':
                messages.error(request, 'پیام خود را وارد کنید')
                return redirect('contact_us')
            obj = Contact_us.objects.create(name=name, phone=phone, message=message, email=email)
            Contact_us.save(obj)
            messages.success(request, 'پیام شما دریافت شد')
            return redirect('contact_us')
        else:
            messages.error(request, 'کپچا نادرست است')
            return redirect('contact_us')
    return render(request, 'contact_us_app/contact_us.html', {'form': form})
