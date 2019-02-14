from django.shortcuts import render
import json
from django.utils.safestring import mark_safe
from django.shortcuts import render
from chat.forms import UserForm
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.models import User
from .tokens import account_activation_token


# this method is used to display the home page
def index(request):
    return render(request, 'chat/indexs.html', {})


@login_required     # only after login of user this method can be called
def enter(request):     # this method is used to enter the chat lobby
        return render(request, 'chat/index.html', {})


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })


@login_required     # only  after login of user this method can be called
def special(request):
    return HttpResponse("You are logged in !")


@login_required    # only after login of user this method can be called
def user_logout(request):       # this method is used to logout
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):      # this method is used to signup the user
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('chat/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                # takes user id and generates the base64 code(uidb64)
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                # Here we receive uidb64, token. By using the "urlsafe_base64_decode"
                # we decode the base64 encoded uidb64 user id.
                # We query the database with user id to get user
                'token': account_activation_token.make_token(user),
                # takes the user object and generates the onetime usable token for the user(token)
            })
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')

    else:
        user_form = UserForm()

    return render(request, 'chat/registration.html',
                           {'user_form': user_form})


def user_login(request):        # this method is used to login the user
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # authentication of user name and password
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return render(request, 'chat/index.html', {})
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'chat/login.html', {})


def activate(request, uidb64, token):   # this method is used to generate confirmation mail to the user
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))  # uid: The user’s primary key encoded in base 64.
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        # We check the token validation
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')



