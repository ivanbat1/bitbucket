from django.template.context_processors import csrf
from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from smtplib import SMTPAuthenticationError


def logowanie(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            args['login_error'] = 'user is not found'
            return render(request, 'login.html', args)
    else:
        return render(request, 'login.html', args)


def logout(request):
    auth.logout(request)
    return redirect("/")


def register(request):
    try:
        form = SignupForm(request.POST or None)
        if request.POST:
            form = SignupForm(request.POST or None)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                message = render_to_string('acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': account_activation_token.make_token(user),
                })
                mail_subject = 'Activate your blog account.'
                to_email = form.cleaned_data.get('email')
                # email = EmailMessage(mail_subject, message, to=[to_email])
                # email.send()
                user.email_user(mail_subject, message)
                return HttpResponse('Please confirm your email address to complete the registration')
        else:
            form = SignupForm()
        return render(request, 'register.html', locals())
    except SMTPAuthenticationError:
        return HttpResponse('<h1>your mail blocks an invitation letter <a href="https://myaccount.google.com/lesssecureapps">tab to change settings</a></h1>')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        user_name = user.username
        # return redirect('home')
        # return redirect('signup/')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.<a href="/">HOME PAGE</a>')
        return render(request, 'activate.html', {'user':user_name})
        # return redirect('login/')
    else:
        return HttpResponse('Activation link is invalid!')