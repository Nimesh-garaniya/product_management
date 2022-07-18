
import django
import logging
from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import CreateView, FormView, TemplateView, View
from .forms import UserRegistrationForm, UserLoginForm

from account.token import account_activation_token
from .models import UserProfile

django.utils.encoding.force_text = force_str

from django.utils.encoding import force_text
log = logging.getLogger(__name__)


class LoginRequiredMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect("account:login")
        return super().dispatch(request, *args, **kwargs)


# class HomeView(TemplateView, LoginRequiredMixin):
#
#     template_name = "account/home.html"


def activate(_, uidb64, token):
    """user confirmation token"""
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        print(user.is_active)
        user.save()
        up = UserProfile.objects.get(email=user.email)
        up.is_active = True
        up.save()
        return HttpResponse(
            "Thank you for your email confirmation. Now you can login your account."
        )
    return HttpResponse("Activation link is invalid!")


class UserRegisterView(CreateView):
    """
        Used to manager User Registrataion view
    """
    model = UserProfile
    template_name = "account/register.html"
    form_class = UserRegistrationForm
    success_url = '/login'
    # add SuccessMessageMixin in class view
    # success_message = 'Account created, please Confirm your mail address!'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("product:ProductList")
        return super(UserRegisterView, self).dispatch(request)

    def form_valid(self, form):
        super().form_valid(form)

        user, created = User.objects.get_or_create(
            email=self.object.email, username=self.object.email
        )

        user.set_password(self.request.POST.get("password1"))
        user.is_active = False
        user.save()

        # for sending mail
        current_site = get_current_site(self.request)

        mail_from = getattr(settings, "EMAIL_HOST_USER", "")
        mail_to = form.cleaned_data.get("email")
        mail_subject = "RealSchool: Account - Email Activation"
        message_body = render_to_string(
            "account/acc_active_email.html",
            {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            },
        )

        try:
            send_mail(
                mail_subject,
                "",
                mail_from,
                [mail_to],
                html_message=message_body,
                fail_silently=False,
            )
            log.info(
                "User Registration Activation Email has been sent to User {user_email}".format(
                    user_email=mail_to
                )
            )
        except Exception as error:
            log.error(
                "Error while sending User Registration Activation Email. {error}".format(
                    error=str(error)
                )
            )

        self.object.user = user
        self.object.save()

        messages.success(
            self.request,
            "Registration successfully. Please verify your email for login",
        )

        return redirect("account:login")


class LoginView(FormView):
    """
        Used to manage User Login view
    """

    form_class = UserLoginForm
    template_name = "account/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("product:ProductList")
        return super(LoginView, self).dispatch(request)

    def form_valid(self, form):

        user = auth.authenticate(**form.cleaned_data)
        if user:
            auth.login(self.request, user)
            return redirect("product:ProductList")
        return redirect("account:login")


class LogoutView(FormView):

    def get(self, *args, **kwargs):
        logout(self.request)
        messages.warning(self.request, "User logged out successfully.")
        return redirect("account:login")
